# The Descript CLI's credentials, and the message that looks like a logged-out session

Split out of `SKILL.md`. Read it the moment the CLI says a credential is not set.

## The CLI is authenticated; load its env before believing otherwise

`pnpm descript` reads `DESCRIPT_STYTCH_SESSION` and `DESCRIPT_API_TOKEN` off the process
environment and loads no `.env` itself. Both live in `vibe-kit/CLIs/.env` and both are valid.
Running the CLI without exporting them prints *"DESCRIPT_STYTCH_SESSION is not set … the
`stytch_session` cookie of a logged-in tab"*, which reads exactly like a logged-out session and is
not one:

```sh
cd ~/Studio/vibe-kit
export DESCRIPT_STYTCH_SESSION="$(grep '^DESCRIPT_STYTCH_SESSION=' CLIs/.env | cut -d= -f2-)"
export DESCRIPT_API_TOKEN="$(grep '^DESCRIPT_API_TOKEN=' CLIs/.env | cut -d= -f2-)"
npx tsx CLIs/descript/cli.ts            # whoami: the user and the five drives
```

On 29 Aug 2026 a session reported that media could not be deleted because "the Orca profile is not
signed in to Descript", and the session was live the whole time. Run the whoami before writing that
sentence. `auth capture --page <orca-page-id>` is for when the cookie has genuinely expired.

## Handing the CLI to somebody else: `pnpm descript connect`

`auth capture` needs Orca, so it is his machine and nobody else's. **`pnpm descript connect` is the
route for anyone**, and it is the one to name when a person has to be walked through this
(2026-08-30). It opens `CLIs/descript/connect.html`, asks for the cookie and then the token on the
terminal, writes both to `CLIs/.env`, and **verifies with a real call** before saying it worked,
because a cookie copied with a stray quote writes just as well as a good one and fails on the next
command instead.

Three things the walkthrough page carries, and the reason each is on a page rather than in a chat
message: the console one-liner
`copy((document.cookie.match(/(?:^|; )stytch_session=([^;]+)/)||[])[1] || "NOT SIGNED IN")` with a
copy button, the DevTools click path for when a console is not an option, and the table saying which
credential does what, so a person who is being asked for a session cookie can see it is a session
and not a password.

**Never take either value as a flag or an argument.** A flag lands in the shell history and in the
process list. The prompt is the interface, and the values are not echoed.
