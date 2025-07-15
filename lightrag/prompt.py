from __future__ import annotations
from typing import Any


PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "Chinese"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["organization", "person", "geo", "event", "category", "road_section", "maintenance_activity", "pavement_condition", "equipment", "material", "weather_condition"]

PROMPTS["DEFAULT_USER_PROMPT"] = "n/a"

PROMPTS["entity_extraction"] = """---Goal---
Given a text document that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.
Use {language} as output language.

---Steps---
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Entity_types: [{entity_types}]
Text:
{input_text}
######################
Output:"""

PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types: [road_section, maintenance_activity, pavement_condition, equipment, material, weather_condition, organization, person, geo]
Text:
```
3月15日，市道路服务处的维修人员对第五大道和第七大道之间的主干道进行了维修，该路段在暴雨后出现了多个坑洼。团队使用一台10吨的沥青摊铺机铺设了5厘米厚的热拌沥青罩面。尽管时有小雨，约翰·多伊还是监督了整个作业过程，确保了振动压路机的正常压实。
```

Output:
("entity"<|>"主干道（第五至第七大道段）"<|>"road_section"<|>"位于第五大道和第七大道之间的一段破损的主干道。")##
("entity"<|>"坑洼"<|>"pavement_condition"<|>"暴雨导致路段出现多个坑洼。")##
("entity"<|>"坑洼修复"<|>"maintenance_activity"<|>"涉及填补坑洼和路面重铺的活动。")##
("entity"<|>"沥青摊铺机"<|>"equipment"<|>"一台10吨的机器，用于在道路上均匀铺设沥青。")##
("entity"<|>"热拌沥青"<|>"material"<|>"用作罩面材料的5厘米厚的热拌沥青。")##
("entity"<|>"小雨"<|>"weather_condition"<|>"维修期间有小雨。")##
("entity"<|>"市道路服务处"<|>"organization"<|>"负责道路养护的市政部门。")##
("entity"<|>"约翰·多伊"<|>"person"<|>"监督养护活动的负责人。")##
("entity"<|>"第五大道和第七大道"<|>"geo"<|>"维修路段的地理参考。")##
("relationship"<|>"市道路服务处"<|>"坑洼修复"<|>"市道路服务处执行了养护活动。"<|>"服务提供商, 执行"<|>"9")##
("relationship"<|>"坑洼修复"<|>"主干道（第五至第七大道段）"<|>"修复活动针对此特定路段。"<|>"目标, 位置"<|>"10")##
("relationship"<|>"坑洼"<|>"主干道（第五至第七大道段）"<|>"该路段存在坑洼。"<|>"道路缺陷, 位置"<|>"8")##
("relationship"<|>"坑洼修复"<|>"沥青摊铺机"<|>"维修期间使用了沥青摊铺机。"<|>"设备使用"<|>"8")##
("relationship"<|>"热拌沥青"<|>"坑洼修复"<|>"在修复活动中用作罩面的材料。"<|>"材料应用"<|>"8")##
("relationship"<|>"小雨"<|>"坑洼修复"<|>"小雨影响了养护期间的工作条件。"<|>"环境条件"<|>"6")##
("relationship"<|>"约翰·多伊"<|>"坑洼修复"<|>"约翰·多伊监督了养护活动。"<|>"监督"<|>"7")##
("content_keywords"<|>"道路养护, 坑洼修复, 沥青罩面, 设备使用, 天气影响")<|COMPLETE|>
#############################""",
    """Example 2:

Entity_types: [road_section, maintenance_activity, pavement_condition, equipment, material, weather_condition]
Text:
```
由于G15高速公路K10+200至K12+500段出现严重车辙，养护单位计划于2023年10月5日至10月10日夜间进行铣刨重铺。施工将使用维特根W2000大型铣刨机和福格勒摊铺机。预计将使用SBS改性沥青混凝土约500吨。期间天气预报为晴天，适合施工。
```

Output:
("entity"<|>"G15高速公路K10+200至K12+500段"<|>"road_section"<|>"G15高速公路的一段，桩号范围从K10+200到K12+500。")##
("entity"<|>"车辙"<|>"pavement_condition"<|>"路段出现严重的车辙病害。")##
("entity"<|>"铣刨重铺"<|>"maintenance_activity"<|>"计划于2023年10月5日至10月10日夜间进行的养护活动，旨在修复车辙。")##
("entity"<|>"维特根W2000大型铣刨机"<|>"equipment"<|>"用于清除旧路面的大型铣刨设备。")##
("entity"<|>"福格勒摊铺机"<|>"equipment"<|>"用于铺设新沥青路面的设备。")##
("entity"<|>"SBS改性沥青混凝土"<|>"material"<|>"本次维修工程计划使用的主要材料，预计用量500吨。")##
("entity"<|>"晴天"<|>"weather_condition"<|>"施工期间的天气状况良好，适合沥青路面施工。")##
("relationship"<|>"铣刨重铺"<|>"G15高速公路K10+200至K12+500段"<|>"铣刨重铺养护活动的目标路段。"<|>"养护对象, 位置"<|>"10")##
("relationship"<|>"车辙"<|>"G15高速公路K10+200至K12+500段"<|>"车辙是该路段需要维修的原因。"<|>"病害, 位置"<|>"9")##
("relationship"<|>"铣刨重铺"<|>"维特根W2000大型铣刨机"<|>"该设备将用于铣刨重铺工程。"<|>"设备使用"<|>"8")##
("relationship"<|>"SBS改性沥青混凝土"<|>"铣刨重铺"<|>"该材料将用于铣刨重铺工程。"<|>"材料应用"<|>"8")##
("relationship"<|>"晴天"<|>"铣刨重铺"<|>"良好的天气是施工的有利条件。"<|>"天气影响, 施工条件"<|>"7")##
("content_keywords"<|>"高速公路养护, 车辙, 铣刨重铺, SBS改性沥青, 施工设备")<|COMPLETE|>
#############################""",
    """Example 3:

Entity_types: [road_section, maintenance_activity, pavement_condition, material]
Text:
```
为预防冬季桥梁结冰，养护团队在S20外环高速的跨海大桥上预撒了融雪剂。本次作业主要针对桥面及匝道，使用了环保型氯化钙融雪剂。
```

Output:
("entity"<|>"S20外环高速跨海大桥"<|>"road_section"<|>"S20外环高速上的一座重要桥梁结构。")##
("entity"<|>"桥面结冰"<|>"pavement_condition"<|>"冬季桥梁可能出现的潜在病害或危险状况。")##
("entity"<|>"预撒融雪剂"<|>"maintenance_activity"<|>"为预防道路结冰而采取的预防性养护措施。")##
("entity"<|>"环保型氯化钙融雪剂"<|>"material"<|>"用于本次预防性养护作业的材料。")##
("relationship"<|>"预撒融雪剂"<|>"S20外环高速跨海大桥"<|>"在跨海大桥上实施了预撒融雪剂作业。"<|>"作业地点, 预防性养护"<|>"10")##
("relationship"<|>"预撒融雪剂"<|>"桥面结冰"<|>"预撒融雪剂的目的是为了防止桥面结冰。"<|>"预防, 病害"<|>"9")##
("relationship"<|>"环保型氯化钙融雪剂"<|>"预撒融雪剂"<|>"该材料被用于预撒融雪剂作业。"<|>"材料使用"<|>"8")##
("content_keywords"<|>"桥梁养护, 预防性养护, 融雪剂, 冬季安全")<|COMPLETE|>
#############################""",
]

PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.
Use {language} as output language.

#######
---Data---
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS["entity_continue_extraction"] = """
MANY entities and relationships were missed in the last extraction.

---Remember Steps---

1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

---Output---

Add them below using the same format:\n
""".strip()

PROMPTS["entity_if_loop_extraction"] = """
---Goal---'

It appears some entities may have still been missed.

---Output---

Answer ONLY by `YES` OR `NO` if there are still entities that need to be added.
""".strip()

PROMPTS["fail_response"] = (
    "Sorry, I'm not able to provide an answer to that question.[no-context]"
)

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to user query about Knowledge Graph and Document Chunks provided in JSON format below.


---Goal---

Generate a concise response based on Knowledge Base and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Knowledge Base, and incorporating general knowledge relevant to the Knowledge Base. Do not include information not provided by Knowledge Base.

When handling relationships with timestamps:
1. Each relationship has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting relationships, consider both the semantic content and the timestamp
3. Don't automatically prefer the most recently created relationships - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Knowledge Graph and Document Chunks---
{context_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- List up to 5 most important reference sources at the end under "References" section. Clearly indicating whether each source is from Knowledge Graph (KG) or Document Chunks (DC), and include the file path if available, in the following format: [KG/DC] file_path
- If you don't know the answer, just say so.
- Do not make anything up. Do not include information not provided by the Knowledge Base.
- Addtional user prompt: {user_prompt}

Response:"""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query and conversation history.

---Goal---

Given the query and conversation history, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Consider both the current query and relevant conversation history when extracting keywords
- Output the keywords in JSON format, it will be parsed by a JSON parser, do not add any extra content in output
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes
  - "low_level_keywords" for specific entities or details

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Conversation History:
{history}

Current Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"
################
Output:
{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}
#############################""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}
#############################""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}
#############################""",
]

PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to user query about Document Chunks provided provided in JSON format below.

---Goal---

Generate a concise response based on Document Chunks and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Document Chunks, and incorporating general knowledge relevant to the Document Chunks. Do not include information not provided by Document Chunks.

When handling content with timestamps:
1. Each piece of content has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content and the timestamp
3. Don't automatically prefer the most recent content - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Document Chunks(DC)---
{content_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- List up to 5 most important reference sources at the end under "References" section. Clearly indicating each source from Document Chunks(DC), and include the file path if available, in the following format: [DC] file_path
- If you don't know the answer, just say so.
- Do not include information not provided by the Document Chunks.
- Addtional user prompt: {user_prompt}

Response:"""

# TODO: deprecated
PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate whether these two questions are semantically similar, and whether the answer to Question 2 can be used to answer Question 1, provide a similarity score between 0 and 1 directly.

Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""
