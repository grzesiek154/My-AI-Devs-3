from HttpService import HttpService
from OpenAIService import OpenAIService
import asyncio

async def main():
    http_service = HttpService()
    openai_service = OpenAIService()

    robotid_json = await http_service.get_raw_data("https://centrala.ag3nts.org/data/a93604b2-40c5-46bd-b562-8fd8fcd47774/robotid.json")
    image_url = await openai_service.generate_image_url(robotid_json["description"])

    print(robotid_json)
    print(image_url)

    await http_service.process_api_request("https://centrala.ag3nts.org/report", {
        "task": "robotid",
        "apikey": "a93604b2-40c5-46bd-b562-8fd8fcd47774",
        "answer": image_url
    })

if __name__ == "__main__":
    asyncio.run(main())


