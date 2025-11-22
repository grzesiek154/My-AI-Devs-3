# Data Formats

- Large Language Models cannot read binary files like PDF or DOCX, requiring conversion to comprehensible formats
- Open formats like **markdown, txt, json, and yaml** are recommended for working with LLMs
- Format conversion is essential when dealing with complex documents
- YAML may be more model-friendly than JSON, with up to 30% fewer tokens according to testing with GPT-4o
- Binary formats require specialized handling and often result in loss of formatting
- Always verify unrestricted access to content, especially with external sources

# Content Processing

- Content transformation includes cleaning, converting, and compressing information
- Chunking (dividing documents into smaller fragments) may cause loss of essential context
- More advanced processing includes analyzing entire documents to generate summaries, notes, or concept lists
- Transformation is not just about token economy but also managing model attention
- Converting between formats (PDF → HTML → markdown) enables editing while preserving structure
- Preprocessing data before sending to the model can improve quality and reduce costs

# Knowledge Sources

- External data can be manually entered into system prompts or appear automatically (e.g., RAG)
- Knowledge bases can be built from scratch with LLM in mind rather than adapting existing sources
- Dynamic memory systems like [mem0](https://github.com/mem0ai/mem0) allow storing information during interaction
- Vector stores (like [faiss](https://github.com/facebookresearch/faiss)) enable efficient retrieval of relevant information
- Knowledge graphs can provide structured navigation for models but may face challenges with duplication
- External sources require synchronization and proper identifier management to maintain connections

# Context Management

- Model APIs are stateless, requiring complete conversation history each time
- Context management involves controlling when and how information is presented to the model
- Keeping all search results in context is impractical due to token limits
- Caching mechanisms can temporarily store retrieved information
- Multi-step processing may be required when information comes from different sources
- Context needs to be dynamically loaded based on the current query requirements

# Integration Methods

- Integration with external APIs enables expanded functionality (e.g., Spotify, search engines)
- Webhooks can trigger model actions in response to external events
- Systems can programmatically verify and correct information (e.g., project ID validation)
- RAG (Retrieval-Augmented Generation) connects models with external knowledge sources
- Integration planning must account for potential errors and include retry mechanisms
- Models can support existing workflows rather than replacing them entirely

# Application Workflows

- Example workflows include automatic task classification in Linear
- Multi-step processes can involve analyzing queries, loading context, and interfacing with external systems
- Autonomous planning allows systems to determine required steps without explicit instructions
- Non-deterministic nature of models requires robust error handling
- Models can be used to transform content into more usable formats for future interactions
- Systems can be designed to support existing activities or partially autonomously execute processes

# External Resources

- [Karpathy&#39;s tweet on model &#34;dreaming&#34;](https://twitter.com/karpathy/status/1733299213503787018?lang=en)
- [Linear task management platform](https://linear.app/)
- [Notion knowledge management](https://www.notion.so/)
- [Notion-to-md conversion package](https://www.npmjs.com/package/notion-to-md)
- [Obsidian knowledge management](https://obsidian.md)
- [Let&#39;s build tokenizer together (video by Andrej Karpathy)](https://www.youtube.com/watch?v=zduSFxRajkE)
- [Neo4J blog: Constructing Knowledge Graphs From Unstructured Text Using LLMs](https://neo4j.com/developer-blog/construct-knowledge-graphs-unstructured-text/)

# Repositories

- [linear](https://github.com/i-am-alice/3rd-devs/tree/main/linear): Example for automatic project assignment in Linear
- [files](https://github.com/i-am-alice/3rd-devs/tree/main/files): Assistant logic for conversation history and memory creation
- [websearch](https://github.com/i-am-alice/3rd-devs/tree/main/websearch): Example of integrating web search with LLM
- [mem0](https://github.com/mem0ai/mem0): Project for dynamic memory in AI assistants
- [faiss](https://github.com/facebookresearch/faiss): Vector store for efficient similarity search
