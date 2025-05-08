import asyncio
import logging
from services.HttpService import HttpService
from services.FileService import FileService
from services.AIService import AIService
from services.ArticleService import ArticleService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Initialize services
        http_service = HttpService()
        file_service = FileService()
        ai_service = AIService(file_service)
        article_service = ArticleService(ai_service, file_service, http_service)

        # URL of the article to process
        article_url = "https://centrala.ag3nts.org/dane/arxiv-draft.html"

        # Process the article
        logger.info(f"Processing article from: {article_url}")
        result = await article_service.process_article(article_url)

        if result["status"] == "success":
            logger.info("Article processing completed successfully")
            logger.info(f"Text analysis: {result['text_analysis']}")
            logger.info(f"Number of images analyzed: {len(result['image_analyses'])}")
            logger.info(f"Unified analysis saved to: article.md")
        else:
            logger.error(f"Error processing article: {result['error']}")

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
