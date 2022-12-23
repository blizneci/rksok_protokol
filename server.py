import sys
import asyncio

from random import choice

from config import ENCODING, PROTOCOL, RESPONSES, PHONES
from validation import validation_server_request


async def process_client_request(reader, writer):
    addr = writer.get_extra_info("peername")
    
    client_request = await reader.readuntil(b'\r\n\r\n')
    """
    client_request = b""
    while True:
        line = await reader.readline()
        client_request += line
        if client_request.endswith(b'\r\n\r\n') or not line:
            break
    """
    decoded_client_request = client_request.decode(ENCODING)
    print(
            "-------------------------------\n" \
            f"RECEIVED FROM CLIENT: {addr}\n" \
            f"ENCODED: {client_request}\n" \
            f"DECODED:{decoded_client_request.strip()}\n" \
            "-------------------------------\n")
    
    validation_response = await validation_server_request(decoded_client_request)


    # response_type = choice(RESPONSES)
    # response_to_client = f"{response_type} {PROTOCOL}"
    # if response_type == "НОРМАЛДЫКС":
    #     phone = choice(PHONES)
    #     response_to_client += f"\r\n{phone}"
    # response_to_client += "\r\n\r\n"

    print(
            "-------------------------------\n" \
            f"RESPONSE TO: {addr}\n" \
            f"ENCODED: {response_to_client.encode(ENCODING)}\n" \
            f"DECODED:{response_to_client.strip()}\n" \
            "-------------------------------\n")
    
    # writer.write(response_to_client.encode(ENCODING))
    # await writer.drain()

    print("Close the connection")
    writer.close()
    await writer.wait_closed()


async def main():
    _, address, port, *_ = sys.argv
    port = int(port)

    server = await asyncio.start_server(process_client_request, address, port)
    print(f"Serving on {address}, port: {port}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt: Server shutdown!")
    except Exception as e:
        print(e)
