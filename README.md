# FastAPI + Mailexam

Minimal [FastAPI](https://fastapi.tiangolo.com/) example that sends test mail through [Mailexam](https://mailexam.io/) SMTP via the Python standard library [`smtplib`](https://docs.python.org/3/library/smtplib.html).

Based on the [Mailexam FastAPI guide](https://wiki.mailexam.ru/en/examples/fastapi/).

## What you need

- A Mailexam account and a project with SMTP credentials.
- Python 3.10+ and pip.

From your Mailexam welcome email or dashboard:

| Variable | Description |
|----------|-------------|
| `MAILEXAM_LOGIN` | SMTP login (for example, `xxxxx`) |
| `MAILEXAM_PASSWORD` | SMTP password (paired with the login) |
| Host | `{MAILEXAM_LOGIN}.mailexam.io` (built automatically in code) |

## Quick start (host)

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

3. Edit `.env`:

```env
MAILEXAM_LOGIN=YOUR_LOGIN
MAILEXAM_PASSWORD=YOUR_PASSWORD
MAILEXAM_PORT=587
MAIL_FROM=noreply@example.test
```

4. Run the server:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

The server listens on `http://127.0.0.1:8000` by default. Interactive API docs: http://127.0.0.1:8000/docs

5. Send a test message:

```bash
curl -X POST http://127.0.0.1:8000/mail/test \
  -H 'Content-Type: application/json' \
  -d '{"to":"user@example.test","subject":"Test","body":"Hello"}'
```

The message appears in the Mailexam dashboard → your project → inbox.

## Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MAILEXAM_LOGIN` | yes | — | SMTP login; also used to build the host name |
| `MAILEXAM_PASSWORD` | yes | — | SMTP password |
| `MAILEXAM_PORT` | no | `587` | SMTP port (`587`, `2525`, or `25`) |
| `MAIL_FROM` | no | `noreply@example.test` | Sender address (any test address is fine) |
| `HTTP_HOST` | no | `127.0.0.1` | HTTP bind address (used in Docker) |
| `HTTP_PORT` | no | `8000` | HTTP listen port (used in Docker) |

For port **587** the code calls `starttls()` before login. For port **25** it connects without STARTTLS.

## Project layout

```
.
├── requirements.txt
├── mail.py            # smtplib transport and send_test()
├── main.py            # FastAPI app and POST /mail/test
├── .env.example
├── Dockerfile         # for local debugging only
└── docker-compose.yml
```

## Docker (debugging)

Docker is provided for local debugging. For day-to-day development, run the app on the host with uvicorn (see above).

```bash
cp .env.example .env
# edit .env with your credentials

docker compose up --build
```

Then call the same endpoint on the mapped port:

```bash
curl -X POST http://127.0.0.1:8000/mail/test \
  -H 'Content-Type: application/json' \
  -d '{"to":"user@example.test","subject":"Test","body":"Hello"}'
```

Inside the container the server binds to `0.0.0.0:8000` so the port mapping works.

## CI

Set these secrets in your CI environment:

```yaml
variables:
  MAILEXAM_LOGIN: $MAILEXAM_LOGIN
  MAILEXAM_PASSWORD: $MAILEXAM_PASSWORD
  MAILEXAM_PORT: "587"
  MAIL_FROM: "noreply@example.test"
```

After sending a message in a test, verify delivery via the [Mailexam API](https://mailexam.io/api).

## Troubleshooting

**TLS or connection error**

- Host must be `{login}.mailexam.io`, where `{login}` matches `MAILEXAM_LOGIN`.
- Login and password must come from the same Mailexam project.
- For port **587** call `starttls()` before `login()`.

**Event loop blocking**

- `send_test()` runs inside `asyncio.to_thread()` so the async handler does not block.

**Message not in the dashboard**

- Open the inbox of the same Mailexam project.
- Check the `/mail/test` response and uvicorn logs.

**Port already in use**

- Change the port in the uvicorn command or set `HTTP_PORT` in Docker.

## See also

- [Mailexam FastAPI guide (wiki)](https://wiki.mailexam.ru/en/examples/fastapi/)
- [Flask reference implementation](https://github.com/mailexam/Flask) — same `mail.py` module, synchronous route
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [Mailexam API documentation](https://mailexam.io/api)
