# crewAI — Knowledge Graph Index
> SHA `d80719d` · 4,256 nodes · 1,463 edges · 2026-06-13

## Quick Navigation
- [[hot]] — God-node hot-spot cache
- [[index]] — This file (domain map)

## Domain Architecture

### a2a (197 classes)

- [[TLSConfig]] · `crewai.a2a.auth.client_schemes.TLSConfig` · in: 0 out: 0 loc: 89 score: **0**
- [[ClientAuthScheme]] · `crewai.a2a.auth.client_schemes.ClientAuthScheme` · in: 0 out: 0 loc: 28 score: **0**
- [[AuthScheme]] · `crewai.a2a.auth.client_schemes.AuthScheme` · in: 0 out: 0 loc: 2 score: **0**
- [[BearerTokenAuth]] · `crewai.a2a.auth.client_schemes.BearerTokenAuth` · in: 0 out: 0 loc: 23 score: **0**
- [[HTTPBasicAuth]] · `crewai.a2a.auth.client_schemes.HTTPBasicAuth` · in: 0 out: 0 loc: 27 score: **0**
- [[HTTPDigestAuth]] · `crewai.a2a.auth.client_schemes.HTTPDigestAuth` · in: 0 out: 0 loc: 44 score: **0**
- [[APIKeyAuth]] · `crewai.a2a.auth.client_schemes.APIKeyAuth` · in: 0 out: 0 loc: 55 score: **0**
- [[OAuth2ClientCredentials]] · `crewai.a2a.auth.client_schemes.OAuth2ClientCredentials` · in: 0 out: 0 loc: 83 score: **0**
- [[OAuth2AuthorizationCode]] · `crewai.a2a.auth.client_schemes.OAuth2AuthorizationCode` · in: 0 out: 0 loc: 149 score: **0**
- [[AuthScheme]] · `crewai.a2a.auth.schemas.AuthScheme` · in: 0 out: 0 loc: 2 score: **0**
- *…and 187 more*

### events (176 classes)

- [[BaseEventListener]] · `crewai.events.base_event_listener.BaseEventListener` · in: 0 out: 0 loc: 18 score: **0**
- [[BaseEvent]] · `crewai.events.base_events.BaseEvent` · in: 0 out: 0 loc: 51 score: **0**
- [[EventHandler]] · `crewai.events.depends.EventHandler` · in: 0 out: 0 loc: 21 score: **0**
- [[Depends]] · `crewai.events.depends.Depends` · in: 0 out: 0 loc: 63 score: **0**
- [[CrewAIEventsBus]] · `crewai.events.event_bus.CrewAIEventsBus` · in: 0 out: 0 loc: 856 score: **0**
- [[MismatchBehavior]] · `crewai.events.event_context.MismatchBehavior` · in: 0 out: 0 loc: 6 score: **0**
- [[EventContextConfig]] · `crewai.events.event_context.EventContextConfig` · in: 0 out: 0 loc: 6 score: **0**
- [[StackDepthExceededError]] · `crewai.events.event_context.StackDepthExceededError` · in: 0 out: 0 loc: 2 score: **0**
- [[EventPairingError]] · `crewai.events.event_context.EventPairingError` · in: 0 out: 0 loc: 2 score: **0**
- [[EmptyStackError]] · `crewai.events.event_context.EmptyStackError` · in: 0 out: 0 loc: 2 score: **0**
- *…and 166 more*

### rag (93 classes)

- [[_RagModule]] · `crewai.rag._RagModule` · in: 0 out: 0 loc: 43 score: **0**
- [[ChromaDBClient]] · `crewai.rag.chromadb.client.ChromaDBClient` · in: 0 out: 0 loc: 610 score: **0**
- [[ChromaDBConfig]] · `crewai.rag.chromadb.config.ChromaDBConfig` · in: 0 out: 0 loc: 10 score: **0**
- [[ChromaEmbeddingFunctionWrapper]] · `crewai.rag.chromadb.types.ChromaEmbeddingFunctionWrapper` · in: 0 out: 0 loc: 13 score: **0**
- [[PreparedDocuments]] · `crewai.rag.chromadb.types.PreparedDocuments` · in: 0 out: 0 loc: 12 score: **0**
- [[ExtractedSearchParams]] · `crewai.rag.chromadb.types.ExtractedSearchParams` · in: 0 out: 0 loc: 22 score: **0**
- [[ChromaDBCollectionCreateParams]] · `crewai.rag.chromadb.types.ChromaDBCollectionCreateParams` · in: 0 out: 0 loc: 12 score: **0**
- [[ChromaDBCollectionSearchParams]] · `crewai.rag.chromadb.types.ChromaDBCollectionSearchParams` · in: 0 out: 0 loc: 10 score: **0**
- [[BaseRagConfig]] · `crewai.rag.config.base.BaseRagConfig` · in: 0 out: 0 loc: 8 score: **0**
- [[_MissingProvider]] · `crewai.rag.config.optional_imports.base._MissingProvider` · in: 0 out: 0 loc: 16 score: **0**
- *…and 83 more*

### flow (57 classes)

- [[ConsoleProvider]] · `crewai.flow.async_feedback.providers.ConsoleProvider` · in: 0 out: 0 loc: 169 score: **0**
- [[PendingFeedbackContext]] · `crewai.flow.async_feedback.types.PendingFeedbackContext` · in: 0 out: 0 loc: 120 score: **0**
- [[HumanFeedbackPending]] · `crewai.flow.async_feedback.types.HumanFeedbackPending` · in: 0 out: 0 loc: 71 score: **0**
- [[HumanFeedbackProvider]] · `crewai.flow.async_feedback.types.HumanFeedbackProvider` · in: 0 out: 0 loc: 77 score: **0**
- [[ConversationalInputs]] · `crewai.flow.conversation.ConversationalInputs` · in: 0 out: 0 loc: 6 score: **0**
- [[ConversationalConfig]] · `crewai.flow.conversation.ConversationalConfig` · in: 0 out: 0 loc: 12 score: **0**
- [[ChatState]] · `crewai.flow.conversation.ChatState` · in: 0 out: 0 loc: 8 score: **0**
- [[FlowConversationalRouterDefinition]] · `crewai.flow.conversational_definition.FlowConversationalRouterDefinition` · in: 0 out: 0 loc: 11 score: **0**
- [[FlowConversationalDefinition]] · `crewai.flow.conversational_definition.FlowConversationalDefinition` · in: 0 out: 0 loc: 15 score: **0**
- [[FlowMethodDecorator]] · `crewai.flow.dsl._types.FlowMethodDecorator` · in: 0 out: 0 loc: 9 score: **0**
- *…and 47 more*

### utilities (53 classes)

- [[SummaryContent]] · `crewai.utilities.agent_utils.SummaryContent` · in: 0 out: 0 loc: 8 score: **0**
- [[NativeToolCallResult]] · `crewai.utilities.agent_utils.NativeToolCallResult` · in: 0 out: 0 loc: 9 score: **0**
- [[_NotSpecified]] · `crewai.utilities.constants._NotSpecified` · in: 0 out: 0 loc: 29 score: **0**
- [[ConverterError]] · `crewai.utilities.converter.ConverterError` · in: 0 out: 0 loc: 12 score: **0**
- [[Converter]] · `crewai.utilities.converter.Converter` · in: 0 out: 0 loc: 146 score: **0**
- [[CreateConverterKwargs]] · `crewai.utilities.converter.CreateConverterKwargs` · in: 0 out: 0 loc: 14 score: **0**
- [[CrewContext]] · `crewai.utilities.crew.models.CrewContext` · in: 0 out: 0 loc: 12 score: **0**
- [[CrewJSONEncoder]] · `crewai.utilities.crew_json_encoder.CrewJSONEncoder` · in: 0 out: 0 loc: 35 score: **0**
- [[DatabaseOperationError]] · `crewai.utilities.errors.DatabaseOperationError` · in: 0 out: 0 loc: 16 score: **0**
- [[DatabaseError]] · `crewai.utilities.errors.DatabaseError` · in: 0 out: 0 loc: 25 score: **0**
- *…and 43 more*

### experimental (36 classes)

- [[AgentExecutorState]] · `crewai.experimental.agent_executor.AgentExecutorState` · in: 0 out: 0 loc: 36 score: **0**
- [[AgentExecutor]] · `crewai.experimental.agent_executor.AgentExecutor` · in: 0 out: 0 loc: 2,932 score: **0**
- [[RouterConfig]] · `crewai.experimental.conversational.RouterConfig` · in: 0 out: 0 loc: 25 score: **0**
- [[ConversationConfig]] · `crewai.experimental.conversational.ConversationConfig` · in: 0 out: 0 loc: 30 score: **0**
- [[ConversationMessage]] · `crewai.experimental.conversational.ConversationMessage` · in: 0 out: 0 loc: 12 score: **0**
- [[AgentMessage]] · `crewai.experimental.conversational.AgentMessage` · in: 0 out: 0 loc: 6 score: **0**
- [[ConversationEvent]] · `crewai.experimental.conversational.ConversationEvent` · in: 0 out: 0 loc: 7 score: **0**
- [[ConversationState]] · `crewai.experimental.conversational.ConversationState` · in: 0 out: 0 loc: 21 score: **0**
- [[_ConversationalMixin]] · `crewai.experimental.conversational_mixin._ConversationalMixin` · in: 0 out: 0 loc: 987 score: **0**
- [[ExecutionState]] · `crewai.experimental.evaluation.agent_evaluator.ExecutionState` · in: 0 out: 0 loc: 9 score: **0**
- *…and 26 more*

### llms (32 classes)

- [[JsonResponseFormat]] · `crewai.llms.base_llm.JsonResponseFormat` · in: 0 out: 0 loc: 4 score: **0**
- [[BaseLLM]] · `crewai.llms.base_llm.BaseLLM` · in: 0 out: 0 loc: 917 score: **0**
- [[BaseInterceptor]] · `crewai.llms.hooks.base.BaseInterceptor` · in: 0 out: 0 loc: 91 score: **0**
- [[HTTPTransportKwargs]] · `crewai.llms.hooks.transport.HTTPTransportKwargs` · in: 0 out: 0 loc: 24 score: **0**
- [[HTTPTransport]] · `crewai.llms.hooks.transport.HTTPTransport` · in: 0 out: 0 loc: 34 score: **0**
- [[AsyncHTTPTransport]] · `crewai.llms.hooks.transport.AsyncHTTPTransport` · in: 0 out: 0 loc: 34 score: **0**
- [[AnthropicThinkingConfig]] · `crewai.llms.providers.anthropic.completion.AnthropicThinkingConfig` · in: 0 out: 0 loc: 3 score: **0**
- [[AnthropicToolSearchConfig]] · `crewai.llms.providers.anthropic.completion.AnthropicToolSearchConfig` · in: 0 out: 0 loc: 14 score: **0**
- [[AnthropicCompletion]] · `crewai.llms.providers.anthropic.completion.AnthropicCompletion` · in: 0 out: 0 loc: 1,789 score: **0**
- [[AzureCompletionParams]] · `crewai.llms.providers.azure.completion.AzureCompletionParams` · in: 0 out: 0 loc: 16 score: **0**
- *…and 22 more*

### agents (30 classes)

- [[BaseAgentAdapter]] · `crewai.agents.agent_adapters.base_agent_adapter.BaseAgentAdapter` · in: 0 out: 0 loc: 32 score: **0**
- [[BaseConverterAdapter]] · `crewai.agents.agent_adapters.base_converter_adapter.BaseConverterAdapter` · in: 0 out: 0 loc: 130 score: **0**
- [[BaseToolAdapter]] · `crewai.agents.agent_adapters.base_tool_adapter.BaseToolAdapter` · in: 0 out: 0 loc: 28 score: **0**
- [[LangGraphAgentAdapter]] · `crewai.agents.agent_adapters.langgraph.langgraph_adapter.LangGraphAgentAdapter` · in: 0 out: 0 loc: 281 score: **0**
- [[LangGraphToolAdapter]] · `crewai.agents.agent_adapters.langgraph.langgraph_tool_adapter.LangGraphToolAdapter` · in: 0 out: 0 loc: 85 score: **0**
- [[LangGraphMemorySaver]] · `crewai.agents.agent_adapters.langgraph.protocols.LangGraphMemorySaver` · in: 0 out: 0 loc: 9 score: **0**
- [[LangGraphCheckPointMemoryModule]] · `crewai.agents.agent_adapters.langgraph.protocols.LangGraphCheckPointMemoryModule` · in: 0 out: 0 loc: 7 score: **0**
- [[LangGraphPrebuiltModule]] · `crewai.agents.agent_adapters.langgraph.protocols.LangGraphPrebuiltModule` · in: 0 out: 0 loc: 27 score: **0**
- [[LangGraphConverterAdapter]] · `crewai.agents.agent_adapters.langgraph.structured_output_converter.LangGraphConverterAdapter` · in: 0 out: 0 loc: 66 score: **0**
- [[OpenAIAgentAdapter]] · `crewai.agents.agent_adapters.openai_agents.openai_adapter.OpenAIAgentAdapter` · in: 0 out: 0 loc: 199 score: **0**
- *…and 20 more*

### tools (28 classes)

- [[AddImageToolSchema]] · `crewai.tools.agent_tools.add_image_tool.AddImageToolSchema` · in: 0 out: 0 loc: 5 score: **0**
- [[AddImageTool]] · `crewai.tools.agent_tools.add_image_tool.AddImageTool` · in: 0 out: 0 loc: 27 score: **0**
- [[AgentTools]] · `crewai.tools.agent_tools.agent_tools.AgentTools` · in: 0 out: 0 loc: 21 score: **0**
- [[AskQuestionToolSchema]] · `crewai.tools.agent_tools.ask_question_tool.AskQuestionToolSchema` · in: 0 out: 0 loc: 4 score: **0**
- [[AskQuestionTool]] · `crewai.tools.agent_tools.ask_question_tool.AskQuestionTool` · in: 0 out: 0 loc: 15 score: **0**
- [[BaseAgentTool]] · `crewai.tools.agent_tools.base_agent_tools.BaseAgentTool` · in: 0 out: 0 loc: 110 score: **0**
- [[DelegateWorkToolSchema]] · `crewai.tools.agent_tools.delegate_work_tool.DelegateWorkToolSchema` · in: 0 out: 0 loc: 6 score: **0**
- [[DelegateWorkTool]] · `crewai.tools.agent_tools.delegate_work_tool.DelegateWorkTool` · in: 0 out: 0 loc: 15 score: **0**
- [[ReadFileToolSchema]] · `crewai.tools.agent_tools.read_file_tool.ReadFileToolSchema` · in: 0 out: 0 loc: 4 score: **0**
- [[ReadFileTool]] · `crewai.tools.agent_tools.read_file_tool.ReadFileTool` · in: 0 out: 0 loc: 78 score: **0**
- *…and 18 more*

### project (23 classes)

- [[AgentConfig]] · `crewai.project.crew_base.AgentConfig` · in: 0 out: 0 loc: 53 score: **0**
- [[TaskConfig]] · `crewai.project.crew_base.TaskConfig` · in: 0 out: 0 loc: 31 score: **0**
- [[CrewBaseMeta]] · `crewai.project.crew_base.CrewBaseMeta` · in: 0 out: 0 loc: 95 score: **0**
- [[_CrewBaseType]] · `crewai.project.crew_base._CrewBaseType` · in: 0 out: 0 loc: 23 score: **0**
- [[CrewBase]] · `crewai.project.crew_base.CrewBase` · in: 0 out: 0 loc: 23 score: **0**
- [[CrewMetadata]] · `crewai.project.wrappers.CrewMetadata` · in: 0 out: 0 loc: 12 score: **0**
- [[TaskResult]] · `crewai.project.wrappers.TaskResult` · in: 0 out: 0 loc: 4 score: **0**
- [[CrewInstance]] · `crewai.project.wrappers.CrewInstance` · in: 0 out: 0 loc: 46 score: **0**
- [[CrewClass]] · `crewai.project.wrappers.CrewClass` · in: 0 out: 0 loc: 20 score: **0**
- [[DecoratedMethod]] · `crewai.project.wrappers.DecoratedMethod` · in: 0 out: 0 loc: 69 score: **0**
- *…and 13 more*

### memory (22 classes)

- [[ExtractedMetadata]] · `crewai.memory.analyze.ExtractedMetadata` · in: 0 out: 0 loc: 17 score: **0**
- [[MemoryAnalysis]] · `crewai.memory.analyze.MemoryAnalysis` · in: 0 out: 0 loc: 20 score: **0**
- [[QueryAnalysis]] · `crewai.memory.analyze.QueryAnalysis` · in: 0 out: 0 loc: 33 score: **0**
- [[ExtractedMemories]] · `crewai.memory.analyze.ExtractedMemories` · in: 0 out: 0 loc: 7 score: **0**
- [[ConsolidationAction]] · `crewai.memory.analyze.ConsolidationAction` · in: 0 out: 0 loc: 19 score: **0**
- [[ConsolidationPlan]] · `crewai.memory.analyze.ConsolidationPlan` · in: 0 out: 0 loc: 17 score: **0**
- [[ItemState]] · `crewai.memory.encoding_flow.ItemState` · in: 0 out: 0 loc: 25 score: **0**
- [[EncodingState]] · `crewai.memory.encoding_flow.EncodingState` · in: 0 out: 0 loc: 9 score: **0**
- [[EncodingFlow]] · `crewai.memory.encoding_flow.EncodingFlow` · in: 0 out: 0 loc: 425 score: **0**
- [[MemoryScope]] · `crewai.memory.memory_scope.MemoryScope` · in: 0 out: 0 loc: 187 score: **0**
- *…and 12 more*

### knowledge (15 classes)

- [[Knowledge]] · `crewai.knowledge.knowledge.Knowledge` · in: 0 out: 0 loc: 118 score: **0**
- [[KnowledgeConfig]] · `crewai.knowledge.knowledge_config.KnowledgeConfig` · in: 0 out: 0 loc: 13 score: **0**
- [[BaseFileKnowledgeSource]] · `crewai.knowledge.source.base_file_knowledge_source.BaseFileKnowledgeSource` · in: 0 out: 0 loc: 104 score: **0**
- [[BaseKnowledgeSource]] · `crewai.knowledge.source.base_knowledge_source.BaseKnowledgeSource` · in: 0 out: 0 loc: 63 score: **0**
- [[_DoclingModules]] · `crewai.knowledge.source.crew_docling_source._DoclingModules` · in: 0 out: 0 loc: 7 score: **0**
- [[CrewDoclingSource]] · `crewai.knowledge.source.crew_docling_source.CrewDoclingSource` · in: 0 out: 0 loc: 111 score: **0**
- [[CSVKnowledgeSource]] · `crewai.knowledge.source.csv_knowledge_source.CSVKnowledgeSource` · in: 0 out: 0 loc: 44 score: **0**
- [[ExcelKnowledgeSource]] · `crewai.knowledge.source.excel_knowledge_source.ExcelKnowledgeSource` · in: 0 out: 0 loc: 170 score: **0**
- [[JSONKnowledgeSource]] · `crewai.knowledge.source.json_knowledge_source.JSONKnowledgeSource` · in: 0 out: 0 loc: 56 score: **0**
- [[PDFKnowledgeSource]] · `crewai.knowledge.source.pdf_knowledge_source.PDFKnowledgeSource` · in: 0 out: 0 loc: 56 score: **0**
- *…and 5 more*

### mcp (13 classes)

- [[_MCPToolResult]] · `crewai.mcp.client._MCPToolResult` · in: 0 out: 0 loc: 5 score: **0**
- [[MCPClient]] · `crewai.mcp.client.MCPClient` · in: 0 out: 0 loc: 695 score: **0**
- [[MCPServerStdio]] · `crewai.mcp.config.MCPServerStdio` · in: 0 out: 0 loc: 39 score: **0**
- [[MCPServerHTTP]] · `crewai.mcp.config.MCPServerHTTP` · in: 0 out: 0 loc: 35 score: **0**
- [[MCPServerSSE]] · `crewai.mcp.config.MCPServerSSE` · in: 0 out: 0 loc: 31 score: **0**
- [[ToolFilterContext]] · `crewai.mcp.filters.ToolFilterContext` · in: 0 out: 0 loc: 13 score: **0**
- [[StaticToolFilter]] · `crewai.mcp.filters.StaticToolFilter` · in: 0 out: 0 loc: 51 score: **0**
- [[MCPToolResolver]] · `crewai.mcp.tool_resolver.MCPToolResolver` · in: 0 out: 0 loc: 596 score: **0**
- [[TransportType]] · `crewai.mcp.transports.base.TransportType` · in: 0 out: 0 loc: 7 score: **0**
- [[BaseTransport]] · `crewai.mcp.transports.base.BaseTransport` · in: 0 out: 0 loc: 91 score: **0**
- *…and 3 more*

### hooks (11 classes)

- [[LLMCallHookContext]] · `crewai.hooks.llm_hooks.LLMCallHookContext` · in: 0 out: 0 loc: 127 score: **0**
- [[ToolCallHookContext]] · `crewai.hooks.tool_hooks.ToolCallHookContext` · in: 0 out: 0 loc: 93 score: **0**
- [[Hook]] · `crewai.hooks.types.Hook` · in: 0 out: 0 loc: 28 score: **0**
- [[BeforeLLMCallHook]] · `crewai.hooks.types.BeforeLLMCallHook` · in: 0 out: 0 loc: 18 score: **0**
- [[AfterLLMCallHook]] · `crewai.hooks.types.AfterLLMCallHook` · in: 0 out: 0 loc: 18 score: **0**
- [[BeforeToolCallHook]] · `crewai.hooks.types.BeforeToolCallHook` · in: 0 out: 0 loc: 18 score: **0**
- [[AfterToolCallHook]] · `crewai.hooks.types.AfterToolCallHook` · in: 0 out: 0 loc: 17 score: **0**
- [[BeforeLLMCallHookMethod]] · `crewai.hooks.wrappers.BeforeLLMCallHookMethod` · in: 0 out: 0 loc: 46 score: **0**
- [[AfterLLMCallHookMethod]] · `crewai.hooks.wrappers.AfterLLMCallHookMethod` · in: 0 out: 0 loc: 24 score: **0**
- [[BeforeToolCallHookMethod]] · `crewai.hooks.wrappers.BeforeToolCallHookMethod` · in: 0 out: 0 loc: 26 score: **0**
- *…and 1 more*

### types (9 classes)

- [[ChatInputField]] · `crewai.types.crew_chat.ChatInputField` · in: 0 out: 0 loc: 13 score: **0**
- [[ChatInputs]] · `crewai.types.crew_chat.ChatInputs` · in: 0 out: 0 loc: 23 score: **0**
- [[StreamChunkType]] · `crewai.types.streaming.StreamChunkType` · in: 0 out: 0 loc: 5 score: **0**
- [[ToolCallChunk]] · `crewai.types.streaming.ToolCallChunk` · in: 0 out: 0 loc: 14 score: **0**
- [[StreamChunk]] · `crewai.types.streaming.StreamChunk` · in: 0 out: 0 loc: 30 score: **0**
- [[StreamingOutputBase]] · `crewai.types.streaming.StreamingOutputBase` · in: 0 out: 0 loc: 163 score: **0**
- [[CrewStreamingOutput]] · `crewai.types.streaming.CrewStreamingOutput` · in: 0 out: 0 loc: 80 score: **0**
- [[FlowStreamingOutput]] · `crewai.types.streaming.FlowStreamingOutput` · in: 0 out: 0 loc: 30 score: **0**
- [[UsageMetrics]] · `crewai.types.usage_metrics.UsageMetrics` · in: 0 out: 0 loc: 93 score: **0**

### state (7 classes)

- [[CheckpointConfig]] · `crewai.state.checkpoint_config.CheckpointConfig` · in: 0 out: 0 loc: 53 score: **0**
- [[EventNode]] · `crewai.state.event_record.EventNode` · in: 0 out: 0 loc: 33 score: **0**
- [[EventRecord]] · `crewai.state.event_record.EventRecord` · in: 0 out: 0 loc: 127 score: **0**
- [[BaseProvider]] · `crewai.state.provider.core.BaseProvider` · in: 0 out: 0 loc: 102 score: **0**
- [[JsonProvider]] · `crewai.state.provider.json_provider.JsonProvider` · in: 0 out: 0 loc: 108 score: **0**
- [[SqliteProvider]] · `crewai.state.provider.sqlite_provider.SqliteProvider` · in: 0 out: 0 loc: 117 score: **0**
- [[RuntimeState]] · `crewai.state.runtime.RuntimeState` · in: 0 out: 0 loc: 321 score: **0**

### core (6 classes)

- [[ContentProcessorProvider]] · `crewai.core.providers.content_processor.ContentProcessorProvider` · in: 0 out: 0 loc: 14 score: **0**
- [[NoOpContentProcessor]] · `crewai.core.providers.content_processor.NoOpContentProcessor` · in: 0 out: 0 loc: 14 score: **0**
- [[ExecutorContext]] · `crewai.core.providers.human_input.ExecutorContext` · in: 0 out: 0 loc: 29 score: **0**
- [[AsyncExecutorContext]] · `crewai.core.providers.human_input.AsyncExecutorContext` · in: 0 out: 0 loc: 6 score: **0**
- [[HumanInputProvider]] · `crewai.core.providers.human_input.HumanInputProvider` · in: 0 out: 0 loc: 85 score: **0**
- [[SyncHumanInputProvider]] · `crewai.core.providers.human_input.SyncHumanInputProvider` · in: 0 out: 0 loc: 276 score: **0**

### tasks (6 classes)

- [[ConditionalTask]] · `crewai.tasks.conditional_task.ConditionalTask` · in: 0 out: 0 loc: 55 score: **0**
- [[HallucinationGuardrail]] · `crewai.tasks.hallucination_guardrail.HallucinationGuardrail` · in: 0 out: 0 loc: 84 score: **0**
- [[LLMGuardrailResult]] · `crewai.tasks.llm_guardrail.LLMGuardrailResult` · in: 0 out: 0 loc: 8 score: **0**
- [[LLMGuardrail]] · `crewai.tasks.llm_guardrail.LLMGuardrail` · in: 0 out: 0 loc: 71 score: **0**
- [[OutputFormat]] · `crewai.tasks.output_format.OutputFormat` · in: 0 out: 0 loc: 12 score: **0**
- [[TaskOutput]] · `crewai.tasks.task_output.TaskOutput` · in: 0 out: 0 loc: 91 score: **0**

### llm (5 classes)

- [[Delta]] · `crewai.llm.Delta` · in: 0 out: 0 loc: 3 score: **0**
- [[StreamingChoices]] · `crewai.llm.StreamingChoices` · in: 0 out: 0 loc: 4 score: **0**
- [[FunctionArgs]] · `crewai.llm.FunctionArgs` · in: 0 out: 0 loc: 3 score: **0**
- [[AccumulatedToolArgs]] · `crewai.llm.AccumulatedToolArgs` · in: 0 out: 0 loc: 2 score: **0**
- [[LLM]] · `crewai.llm.LLM` · in: 0 out: 0 loc: 2,303 score: **0**

### crews (4 classes)

- [[CrewOutput]] · `crewai.crews.crew_output.CrewOutput` · in: 0 out: 0 loc: 48 score: **0**
- [[TaskExecutionData]] · `crewai.crews.utils.TaskExecutionData` · in: 0 out: 0 loc: 19 score: **0**
- [[StreamingContext]] · `crewai.crews.utils.StreamingContext` · in: 0 out: 0 loc: 21 score: **0**
- [[ForEachStreamingContext]] · `crewai.crews.utils.ForEachStreamingContext` · in: 0 out: 0 loc: 17 score: **0**

### agent (3 classes)

- [[Agent]] · `crewai.agent.core.Agent` · in: 0 out: 0 loc: 1,782 score: **0**
- [[AgentMeta]] · `crewai.agent.internal.meta.AgentMeta` · in: 0 out: 0 loc: 68 score: **0**
- [[PlanningConfig]] · `crewai.agent.planning_config.PlanningConfig` · in: 0 out: 0 loc: 138 score: **0**

### skills (3 classes)

- [[SkillFrontmatter]] · `crewai.skills.models.SkillFrontmatter` · in: 0 out: 0 loc: 51 score: **0**
- [[Skill]] · `crewai.skills.models.Skill` · in: 0 out: 0 loc: 82 score: **0**
- [[SkillParseError]] · `crewai.skills.parser.SkillParseError` · in: 0 out: 0 loc: 2 score: **0**

### cli (2 classes)

- [[_ShimLoader]] · `crewai.cli._ShimLoader` · in: 0 out: 0 loc: 11 score: **0**
- [[_ShimFinder]] · `crewai.cli._ShimFinder` · in: 0 out: 0 loc: 27 score: **0**

### lite_agent_output (2 classes)

- [[TodoExecutionResult]] · `crewai.lite_agent_output.TodoExecutionResult` · in: 0 out: 0 loc: 15 score: **0**
- [[LiteAgentOutput]] · `crewai.lite_agent_output.LiteAgentOutput` · in: 0 out: 0 loc: 89 score: **0**

### security (2 classes)

- [[Fingerprint]] · `crewai.security.fingerprint.Fingerprint` · in: 0 out: 0 loc: 117 score: **0**
- [[SecurityConfig]] · `crewai.security.security_config.SecurityConfig` · in: 0 out: 0 loc: 68 score: **0**

### telemetry (2 classes)

- [[SafeOTLPSpanExporter]] · `crewai.telemetry.telemetry.SafeOTLPSpanExporter` · in: 0 out: 0 loc: 21 score: **0**
- [[Telemetry]] · `crewai.telemetry.telemetry.Telemetry` · in: 0 out: 0 loc: 982 score: **0**

### context (1 classes)

- [[ExecutionContext]] · `crewai.context.ExecutionContext` · in: 0 out: 0 loc: 15 score: **0**

### crew (1 classes)

- [[Crew]] · `crewai.crew.Crew` · in: 0 out: 0 loc: 2,197 score: **0**

### lite_agent (1 classes)

- [[LiteAgent]] · `crewai.lite_agent.LiteAgent` · in: 0 out: 0 loc: 800 score: **0**

### mypy (1 classes)

- [[CrewAIPlugin]] · `crewai.mypy.CrewAIPlugin` · in: 0 out: 0 loc: 36 score: **0**

### process (1 classes)

- [[Process]] · `crewai.process.Process` · in: 0 out: 0 loc: 7 score: **0**

### task (1 classes)

- [[Task]] · `crewai.task.Task` · in: 0 out: 0 loc: 1,350 score: **0**
