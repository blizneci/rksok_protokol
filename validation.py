import asyncio

from config import (PROTOCOL, ENCODING, VALIDATION_SERVER_URL, VALIDATION_SERVER_PORT)


async def validation_server_request(message: str) -> str:
    reader, writer = await asyncio.open_connection(
        VALIDATION_SERVER_URL, VALIDATION_SERVER_PORT)
    validation_request = f"АМОЖНА? {PROTOCOL}\r\n{message}"
    writer.write(validation_request.encode(ENCODING))
    await writer.drain()

    validation_response = await reader.readuntil(b'\r\n\r\n')
    """
    response = b""
    while True:
        line = await reader.readline()
        response += line
        if response.endswith(b"\r\n\r\n") or not line:
            break
    """

    writer.close()
    await writer.wait_closed()

    print(f"\nREQUEST_TO_VALIDATION_SERVER:\n{validation_request}")
    print(f"\nRESPONSE_FROM_VALIDATION_SERVER:\n{validation_response.decode(ENCODING)}")

    return validation_response.decode(ENCODING)

if __name__ == "__main__":
    verb = input("Введи тип запроса:\n")
    name = input("Введи имя:\n")
    message = " ".join((verb, name, PROTOCOL))
    if verb == "ЗОПИШИ":
        while True:
            phone = input("Введи телефон:\n")
            if not phone:
                break
            message = "\r\n".join((message, phone))
    asyncio.run(validation_server_request(message))
