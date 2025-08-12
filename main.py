from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse
from schemas import AnalysisResponse
from analysis import TextAnalyzer
from config import MAX_INPUT_SIZE
from logging_config import setup_logging, logger
import json

setup_logging()
app = FastAPI(
    title="String Analysis API",
    description="Submit string inputs for analysis"
)

@app.post(
    "/analyze",
    response_model=AnalysisResponse,
    summary="Analyze text input (plain text or JSON)",
    description=(
        "Accepts either:\n"
        "- Raw plain text in the body, or\n"
        '- JSON with a "text" field.\n\n'
        "Specify analyses as query parameters, e.g., `?analyses=word_count&analyses=char_count`.\n\n"
        "Supported analyses:\n"
        "- word_count\n"
        "- char_count\n"
        "- unique_words\n"
        "- line_count\n"
        "- sentence_count\n"
        "- most_common_word\n"
        "- vowel_count\n"
        "- digit_count\n"
        "- special_char_count"
    ),
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "example": "Hello world! This is an API example."}
                        },
                        "required": ["text"],
                    },
                    "example": {"text": "Hello world! This is an API example."},
                },
                "text/plain": {
                    "schema": {"type": "string", "example": "Hello world! This is an API example."},
                    "example": "Hello world! This is an API example.",
                },
            },
            "required": True,
        }
    }
)


async def analyze(
    request: Request,
    analyses: list[str] = Query(
        ...,
        description=(
            "List of analyses to perform. Supported analyses:\n"
            "- word_count\n"
            "- char_count\n"
            "- unique_words\n"
            "- line_count\n"
            "- sentence_count\n"
            "- most_common_word\n"
            "- vowel_count\n"
            "- digit_count\n"
            "- special_char_count"
        )
    )
):
    """
    Analyze a string using selected analysis options.

    Query Parameters:
    - analyses: List of analysis types to perform (choose from the supported analyses above)

    Request Body:
    - JSON with a "text" field, OR raw plain text

    Response:
    - JSON with results of selected analyses
    """
    try:
        raw_body = await request.body()
        if not raw_body:
            raise HTTPException(status_code=400, detail="Empty request body")

        content_type = request.headers.get("content-type", "")

        if "application/json" in content_type:
            try:
                data = json.loads(raw_body)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON")

            if not (isinstance(data, dict) and "text" in data):
                raise HTTPException(status_code=400, detail="JSON must contain 'text' field")

            text = data["text"]

        else:  # treat as plain text
            text = raw_body.decode("utf-8").strip()
            if not text:
                raise HTTPException(status_code=400, detail="Empty text input")

        if len(text) > MAX_INPUT_SIZE:
            raise HTTPException(status_code=413, detail=f"Input exceeds {MAX_INPUT_SIZE} character limit")

        obj = TextAnalyzer(text)

        # Catch unsupported analysis errors thrown by TextAnalyzer.analyze
        try:
            result = obj.analyze(analyses)
        except Exception as e:
            # If the exception message contains unsupported analysis info,
            # return 400 Bad Request with that message
            msg = str(e)
            if "Unsupported analysis type" in msg:
                raise HTTPException(status_code=400, detail=msg)
            raise

        logger.info(f"Analysis completed successfully: {analyses}")
        return JSONResponse(content=result)

    except HTTPException as http_exc:
        logger.warning(f"Client error: {http_exc.detail}")
        raise http_exc

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
