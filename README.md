# String Analysis API

A FastAPI-based API that accepts string inputs (either raw plain text or JSON with a `"text"` field) and performs a variety of text analyses. Users specify which analyses to perform via query parameters.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Supported Analyses](#supported-analyses)
- [API Endpoint](#api-endpoint)
- [Request Formats](#request-formats)
- [Query Parameters](#query-parameters)

## Overview

The String Analysis API allows clients to submit text strings for detailed analysis. The API supports both plain text and JSON input formats and provides flexible options for selecting which analyses to perform on the input text.

## Features

- Accepts raw plain text or JSON payloads with a `"text"` field
- Supports multiple text analysis types, specified as query parameters
- Limits input size to prevent overly large requests (configurable)
- Provides clear error messages and status codes
- Logs requests, errors, and internal operations

## Supported Analyses

Clients can request any combination of the following analyses via the `analyses` query parameter:

- `word_count` — Count of words in the text
- `char_count` — Count of characters in the text
- `unique_words` — Number of unique words
- `line_count` — Number of lines
- `sentence_count` — Number of sentences
- `most_common_word` — The most frequently occurring word
- `vowel_count` — Count of vowels
- `digit_count` — Count of digit characters
- `special_char_count` — Count of special characters (non-alphanumeric)

## API Endpoint

### `POST /analyze`

Analyze a string input according to requested analyses.

#### Query Parameters

- `analyses` (required): One or more of the supported analyses listed above.

Example: `POST /analyze?analyses=word_count&analyses=char_count`

#### Request Body

Accepts either JSON with the structure:

```json
{
  "text": "Your input string here."
}
