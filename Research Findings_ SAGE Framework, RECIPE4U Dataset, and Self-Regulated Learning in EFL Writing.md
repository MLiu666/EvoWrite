# Research Findings: SAGE Framework, RECIPE4U Dataset, and Self-Regulated Learning in EFL Writing

## Executive Summary

This research document synthesizes findings from three key academic sources to inform the development of a self-evolving multi-agent web page for promoting Chinese EFL learners' self-regulated writing learning. The system will integrate the SAGE (Self-evolving Agents with Reflective and Memory-augmented Abilities) framework [1], the RECIPE4U dataset [2], and principles from validated self-regulated learning strategies for EFL writing [3].

## 1. SAGE Framework Analysis

### 1.1 Framework Overview

The SAGE framework represents a significant advancement in large language model (LLM) applications, specifically designed to address persistent challenges in dynamic environments including continuous decision-making, long-term memory retention, and constrained context windows [1]. The framework comprises three collaborative agents that work in concert to enhance multi-tasking and long-context capabilities through adaptive strategy adjustment, optimized information storage, and reduced cognitive load.

### 1.2 Core Components

The SAGE architecture consists of three primary agents:

**User Agent**: This component serves as the primary interface between human users and the system, responsible for interpreting user inputs, maintaining conversation context, and facilitating natural language interactions. The User Agent acts as the entry point for all educational interactions and learning requests.

**Assistant Agent**: The Assistant Agent functions as the primary problem-solving and content generation component. It processes educational queries, generates writing feedback, provides learning recommendations, and delivers instructional content. This agent leverages the underlying LLM capabilities to provide substantive educational support.

**Checker Agent**: The Checker Agent serves a quality assurance and validation role, reviewing outputs from the Assistant Agent for accuracy, appropriateness, and educational value. This component implements reflective reasoning mechanisms to ensure high-quality educational interactions and maintains consistency across learning sessions.

### 1.3 Key Innovations

The SAGE framework introduces several transformative innovations that make it particularly suitable for educational applications:

**Memory Syntax Mechanism**: This innovation reduces computational overhead by 47% while maintaining comprehensive interaction history. The mechanism implements an optimized information storage system based on the Ebbinghaus forgetting curve, ensuring that relevant educational content is retained while less important information is gradually deprioritized.

**Reflective Reasoning Module**: The reflection module successfully resolves 73.6% of ambiguous references in dialogue tasks, making it particularly valuable for educational contexts where clarity and precision are essential. This capability ensures that learning interactions remain coherent and productive even across extended sessions.

**Iterative Feedback Integration**: The framework implements sophisticated feedback loops that enable continuous improvement of educational interactions. This mechanism allows the system to adapt to individual learning patterns and preferences over time.

### 1.4 Performance Metrics

Evaluations across AgentBench and long-text tasks demonstrate substantial improvements across multiple model types. Closed-source models like GPT-4 achieve 2.26× performance gains in database operations, while open-source models exhibit 5.0–48.0 absolute percentage point improvements. Notably, smaller models such as Qwen-1.8B achieve performance levels comparable to GPT-3.5, demonstrating the framework's ability to enhance model capabilities regardless of base model size.

In practical applications, SAGE shows remarkable improvements in customer support scenarios with 45.3% improvement on WebShop tasks and healthcare diagnostics with 22.06 F1 score on HotpotQA. These results indicate strong potential for educational applications where similar complex reasoning and sustained interaction capabilities are required.

## 2. RECIPE4U Dataset Analysis

### 2.1 Dataset Overview

The RECIPE4U (RECIPE for University) dataset represents a comprehensive collection of student-ChatGPT interactions within the context of English as a Foreign Language (EFL) writing education [2]. This dataset was compiled from a semester-long experiment involving 212 college students and provides unprecedented insights into how EFL learners interact with AI-powered writing assistance tools.

### 2.2 Dataset Composition

The dataset contains 504 dialogues comprising 4,330 total utterances and 380,364 tokens with 16,118 unique tokens. The data spans three different course levels: Intermediate Reading & Writing (IRW), Advanced Writing (AW), and Scientific Writing (SW), providing a comprehensive view of EFL writing education across proficiency levels.

### 2.3 Data Structure and Attributes

The RECIPE4U dataset includes thirteen key attributes that capture the full context of student-AI interactions:

**Identification Fields**: Each interaction is uniquely identified through sample_id, which combines student_id, course, week, session, and utterance index (idx). This hierarchical structure enables detailed analysis of learning progression over time.

**Temporal Context**: The dataset captures the temporal dimension of learning through week and session numbers, allowing for analysis of how student-AI interactions evolve throughout a semester-long learning process.

**Interaction Content**: The core of each record consists of three conversational elements: chatgpt_before (ChatGPT's utterance before student input), user (student's utterance), and chatgpt_after (ChatGPT's response to student input). This structure captures the full conversational flow and enables analysis of how AI responses influence subsequent student interactions.

**Quality Metrics**: Each interaction includes a student's self-rated satisfaction score on a 5-Likert scale, providing direct feedback on the perceived value of AI assistance from the learner's perspective.

**Behavioral Annotations**: The dataset includes several boolean flags that capture specific learning behaviors: is_quiz (whether students asked for quiz answers), and is_essay_edit (whether students made edits to their essays following AI feedback). These annotations enable analysis of how AI interactions translate into actual learning behaviors.

**Intent Classification**: Each student utterance is annotated with intent_final, providing insight into the purposes behind student-AI interactions and enabling analysis of how different interaction types contribute to learning outcomes.

**Essay Content**: The dataset includes the actual essays written by students, enabling analysis of writing quality improvements and the relationship between AI interactions and writing outcomes.

### 2.4 Multilingual Characteristics

The dataset includes both English and Korean content, reflecting the bilingual nature of EFL learning environments. This characteristic is particularly valuable for developing systems that can support learners who may need to code-switch between their native language and English during the learning process.

### 2.5 Educational Context

The semester-long data collection provides insights into sustained learning processes rather than isolated interactions. This temporal depth enables analysis of how student-AI interaction patterns evolve as learners become more familiar with AI assistance tools and as their writing proficiency develops over time.

## 3. Self-Regulated Learning in EFL Writing

### 3.1 Theoretical Foundation

The research by Teng and Zhang [3] provides crucial theoretical grounding for understanding self-regulated learning (SRL) in EFL writing contexts. Their work validates a comprehensive framework for understanding how Chinese EFL learners can effectively regulate their writing learning processes through strategic approaches.

### 3.2 Validated SRL Framework

The study validates a nine-factor correlated model of second language writing strategies for self-regulated learning, encompassing four key dimensions:

**Cognitive Strategies**: These strategies involve direct manipulation of learning materials and include techniques such as elaboration, organization, and critical thinking. In the context of EFL writing, cognitive strategies might involve analyzing model texts, practicing specific grammatical structures, or experimenting with different rhetorical patterns.

**Metacognitive Strategies**: These higher-order strategies involve planning, monitoring, and evaluating learning processes. Metacognitive strategies in EFL writing include setting writing goals, monitoring writing progress, evaluating writing quality, and adjusting writing strategies based on performance feedback.

**Social-Behavioral Strategies**: These strategies involve seeking help from others and managing the learning environment. In EFL writing contexts, social-behavioral strategies include seeking feedback from peers or instructors, participating in writing groups, and creating conducive writing environments.

**Motivational Regulation**: These strategies involve managing motivation, emotions, and persistence in learning. Motivational regulation strategies help EFL writers maintain engagement with challenging writing tasks and persist through difficulties in the writing process.

### 3.3 Predictive Validity

The research demonstrates that six out of nine SRL strategies have significant predictive effects on EFL writing proficiency, providing empirical evidence for the practical value of self-regulated learning approaches in EFL writing education. This finding suggests that systems designed to promote self-regulated learning can have measurable impacts on writing outcomes.

### 3.4 Hierarchical Structure

The validated model confirms a hierarchical, multidimensional structure where self-regulation serves as a higher-order construct that accounts for correlations among the nine lower-order writing strategies. This hierarchical structure provides a theoretical framework for designing educational interventions that target multiple levels of self-regulation simultaneously.

### 3.5 Cultural Context

The research specifically focuses on Chinese EFL learners, providing culturally relevant insights for the target population. The findings suggest that self-regulated learning strategies can be effectively adapted to Chinese educational contexts while maintaining their theoretical integrity and practical effectiveness.

## 4. Integration Opportunities

### 4.1 SAGE-RECIPE4U Synergy

The SAGE framework's memory-augmented capabilities align perfectly with the longitudinal nature of the RECIPE4U dataset. The framework's ability to maintain long-term interaction history can leverage the semester-long interaction patterns documented in RECIPE4U to provide more contextually aware and personalized learning support.

### 4.2 Self-Regulated Learning Enhancement

The validated SRL strategies from Teng and Zhang's research can be operationalized through the SAGE framework's three-agent architecture. The User Agent can facilitate metacognitive strategy development, the Assistant Agent can provide cognitive strategy support, and the Checker Agent can promote reflective evaluation practices.

### 4.3 Adaptive Learning Pathways

The combination of SAGE's adaptive capabilities, RECIPE4U's interaction patterns, and validated SRL strategies creates opportunities for developing truly personalized learning pathways that adapt to individual learner needs, preferences, and progress patterns.

## References

[1] Liang, X., Tao, M., Xia, Y., Wang, J., Li, K., Wang, Y., He, Y., et al. (2025). SAGE: Self-evolving Agents with Reflective and Memory-augmented Abilities. Neurocomputing, 647, 130470. https://doi.org/10.1016/j.neucom.2025.130470

[2] Han, J., Yoo, H., Myung, J., Kim, M., Lee, T. Y., Ahn, S. Y., & Oh, A. (2024). RECIPE4U: Student-ChatGPT Interaction Dataset in EFL Writing Education. In Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024) (pp. 13666-13676). https://aclanthology.org/2024.lrec-main.1193

[3] Teng, L. S., & Zhang, L. J. (2016). A questionnaire‐based validation of multidimensional models of self‐regulated learning strategies. The Modern Language Journal, 100(3), 674-701. https://doi.org/10.1111/modl.12339

