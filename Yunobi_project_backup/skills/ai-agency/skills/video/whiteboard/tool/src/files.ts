import { deflateSync } from "node:zlib";

/**
 * Image transport for the collaboration protocol.
 *
 * WHY THIS EXISTS: `server-broadcast` carries elements only. An image element
 * is a reference - it names a `fileId` and nothing else - so a board pushed
 * without its files arrives as empty frames. The bytes travel out of band:
 * every client encrypts them with the room key and PUTs them into Excalidraw's
 * storage bucket under `files/rooms/<roomId>/<fileId>`, and a peer that meets
 * an unknown fileId fetches it from there.
 *
 * The bucket and its web API key are the public config excalidraw.com ships in
 * its own bundle. The room key never leaves this machine, so the bucket holds
 * ciphertext it cannot read, exactly as it does for the browser client.
 */

const BUCKET = "excalidraw-room-persistence.appspot.com";
const STORAGE = "https://firebasestorage.googleapis.com/v0/b";

// The client refuses anything larger, so an oversized file is a push that
// silently draws an empty frame on the other side.
export const MAX_FILE_BYTES = 4 * 1024 * 1024;

export type SceneFile = { id: string; dataURL: string; mimeType: string };

/**
 * Excalidraw's length-prefixed container: a uint32 version, then each chunk as
 * a uint32 byte length followed by its bytes. Both the outer file and the
 * payload inside the encryption use it.
 */
function concatBuffers(...buffers: Uint8Array[]) {
  const HEADER = 4;
  const CHUNK = 4;
  const total = HEADER + CHUNK * buffers.length + buffers.reduce((sum, b) => sum + b.byteLength, 0);
  const out = new Uint8Array(total);
  const view = new DataView(out.buffer);

  view.setUint32(0, 1);
  let offset = HEADER;
  for (const buffer of buffers) {
    view.setUint32(offset, buffer.byteLength);
    offset += CHUNK;
    out.set(buffer, offset);
    offset += buffer.byteLength;
  }
  return out;
}

async function encrypt(key: string, data: Uint8Array<ArrayBuffer>) {
  const cryptoKey = await crypto.subtle.importKey(
    "jwk",
    { alg: "A128GCM", ext: true, k: key, key_ops: ["encrypt", "decrypt"], kty: "oct" },
    { name: "AES-GCM", length: 128 },
    false,
    ["encrypt"],
  );
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const buffer = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, cryptoKey, data);
  return { iv, buffer: new Uint8Array(buffer) };
}

/**
 * The on-disk shape the client decodes: `[encoding header][iv][AES-GCM(deflate(
 * [metadata][dataURL]))]`. `compression: 'pako@1'` is zlib-wrapped deflate,
 * which is what `zlib.deflateSync` writes, so no pako dependency is needed.
 */
export async function encodeFile(file: SceneFile, key: string) {
  const contents = new TextEncoder().encode(file.dataURL);
  if (contents.byteLength > MAX_FILE_BYTES) {
    throw new Error(
      `${file.id} is ${Math.round(contents.byteLength / 1024)}KB, over the 4MB limit`,
    );
  }

  const header = new TextEncoder().encode(
    JSON.stringify({ version: 2, compression: "pako@1", encryption: "AES-GCM" }),
  );
  const metadata = new TextEncoder().encode(
    JSON.stringify({
      id: file.id,
      mimeType: file.mimeType,
      created: Date.now(),
      lastRetrieved: Date.now(),
    }),
  );
  const deflated = new Uint8Array(deflateSync(concatBuffers(metadata, contents)));
  const { iv, buffer } = await encrypt(key, deflated);
  return concatBuffers(header, iv, buffer);
}

function objectPath(roomId: string, fileId: string) {
  return encodeURIComponent(`files/rooms/${roomId}/${fileId}`);
}

/** Uploads one encoded file. Resolves to the storage path the client will read. */
export async function uploadFile(roomId: string, fileId: string, body: Uint8Array) {
  const url = `${STORAGE}/${BUCKET}/o?uploadType=media&name=${objectPath(roomId, fileId)}`;
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/octet-stream" },
    // WHY the copy: fetch takes an ArrayBuffer, and a Uint8Array view can sit
    // on a larger buffer, so handing over `body.buffer` can send trailing bytes.
    body: body.slice().buffer as ArrayBuffer,
  });
  if (!response.ok) {
    throw new Error(`upload ${fileId} failed: ${response.status} ${await response.text()}`);
  }
  return (await response.json()) as { name: string; size: string };
}

/** Reads an uploaded file back, so a push can prove the bytes are fetchable. */
export async function fetchFile(roomId: string, fileId: string) {
  const url = `${STORAGE}/${BUCKET}/o/${objectPath(roomId, fileId)}?alt=media`;
  const response = await fetch(url);
  if (!response.ok) throw new Error(`fetch ${fileId} failed: ${response.status}`);
  return new Uint8Array(await response.arrayBuffer());
}
