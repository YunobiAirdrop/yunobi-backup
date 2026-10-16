import { io, type Socket } from "socket.io-client";

/**
 * Client for Excalidraw's live collaboration protocol, the same one
 * excalidraw.com and ExcalidrawZ speak.
 *
 * A room link carries both halves of the secret in its fragment:
 * https://excalidraw.com/#room=<roomId>,<encryptionKey>. Payloads are
 * AES-GCM-128 encrypted with that key, so the relay server never sees content.
 */

const SERVER = "https://oss-collab.excalidraw.com";

export type Room = { id: string; key: string };

export function parseRoomLink(link: string): Room {
  const fragment = link.includes("#") ? link.slice(link.indexOf("#") + 1) : link;
  const value = new URLSearchParams(fragment).get("room") ?? fragment;
  const [id, key] = value.split(",");

  if (!id || !key) throw new Error(`Not a room link: ${link}`);
  return { id, key };
}

async function encrypt(key: string, payload: unknown) {
  const cryptoKey = await crypto.subtle.importKey(
    "jwk",
    { alg: "A128GCM", ext: true, k: key, key_ops: ["encrypt", "decrypt"], kty: "oct" },
    { name: "AES-GCM", length: 128 },
    false,
    ["encrypt"],
  );
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const data = new TextEncoder().encode(JSON.stringify(payload));
  const buffer = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, cryptoKey, data);
  return { buffer, iv };
}

export async function decrypt(key: string, buffer: ArrayBuffer, iv: Uint8Array<ArrayBuffer>) {
  const cryptoKey = await crypto.subtle.importKey(
    "jwk",
    { alg: "A128GCM", ext: true, k: key, key_ops: ["encrypt", "decrypt"], kty: "oct" },
    { name: "AES-GCM", length: 128 },
    false,
    ["decrypt"],
  );
  const data = await crypto.subtle.decrypt({ name: "AES-GCM", iv }, cryptoKey, buffer);
  return JSON.parse(new TextDecoder().decode(data));
}

/**
 * Joins a room and resolves once the server has us in it, with the number of
 * other clients already there.
 *
 * WHY the count matters: the relay forwards messages and stores nothing. A
 * broadcast into a room with nobody in it is delivered to nobody and cannot be
 * recovered, and the socket reports the send as fine, so the caller has to
 * check for an audience before it can honestly claim to have drawn anything.
 */
export function join(room: Room): Promise<{ socket: Socket; peers: number }> {
  // WHY: the relay checks Origin, and node-side socket.io sends none by default.
  const socket = io(SERVER, {
    transports: ["websocket"],
    extraHeaders: { Origin: "https://excalidraw.com" },
  });

  return new Promise((resolve, reject) => {
    socket.on("init-room", () => socket.emit("join-room", room.id));
    socket.on("room-user-change", (users: string[]) =>
      resolve({ socket, peers: Math.max(0, (users?.length ?? 1) - 1) }),
    );
    socket.on("connect_error", reject);
  });
}

/**
 * Broadcasts a full scene to everyone else in the room, as both message types.
 *
 * WHY both: a receiving client reconciles a SCENE_UPDATE against the scene it
 * already holds, and only treats SCENE_INIT as the scene for a room it has not
 * seen. Sending UPDATE alone reaches a client that is already collaborating and
 * is dropped by one that has just opened the room, which is the silent failure
 * where the push reports every element sent and the canvas stays blank. INIT is
 * processed once per client, so the repeat on later chunks costs nothing.
 */
export async function broadcast(socket: Socket, room: Room, elements: unknown[]) {
  for (const type of ["SCENE_INIT", "SCENE_UPDATE"]) {
    const { buffer, iv } = await encrypt(room.key, { type, payload: { elements } });
    socket.emit("server-broadcast", room.id, buffer, iv);
  }
}
