# Prϵϵmpt: Sanitizing Sensitive Prompts for LLMs

Amrita Roy Chowdhury∗

University of Michigan, Ann Arbor

David Glukhov∗

University of Toronto and Vector Institute

Divyam Anshumaan∗

University of Wisconsin-Madison

Prasad Chalasani

Langroid Incorporated

Nicolas Papernot

University of Toronto and Vector Institute

Somesh Jha

University of Wisconsin-Madison

Mihir Bellare

University of California, San Diego

August 18, 2025

# ABSTRACT

The rise of large language models (LLMs) has introduced new privacy challenges, particularly during inference where sensitive information in prompts may be exposed to proprietary LLM APIs. In this paper, we address the problem of formally protecting the sensitive information contained in a prompt while maintaining response quality. To this end, first, we introduce a cryptographically inspired notion of a prompt sanitizer which transforms an input prompt to protect its sensitive tokens. Second, we propose Prϵϵmpt, a novel system that implements a prompt sanitizer, focusing on the sensitive information that can be derived solely from the individual tokens. Prϵϵmpt categorizes sensitive tokens into two types: (1) those where the LLM’s response depends solely on the format (such as SSNs, credit card numbers), for which we use format-preserving encryption (FPE); and (2) those where the response depends on specific values, (such as age, salary) for which we apply metric differential privacy (mDP). Our evaluation demonstrates that Prϵϵmpt is a practical method to achieve meaningful privacy guarantees, while maintaining high utility compared to unsanitized prompts, and outperforming prior methods.

# 1 Introduction

The recent advent of large language models (LLMs) have brought forth a fresh set of challenges for protecting users’ data privacy. LLMs and their APIs present significant privacy concerns at inference time, which are fundamentally distinct from the well-documented risks of training data memorization [19, 50, 64, 98]. While the potential adversary in training data scenarios could be any API user, the threat during inference primarily stems from the model owner—typically the organization hosting the LLM. This inference stage poses a significant privacy risk, as prompts in natural language may include various types of sensitive information, from personally identifiable data like SSNs or credit card numbers to personal health or financial details.

The ensuing privacy threat is exacerbated with the growing use of in-context learning, that involves presenting the LLM with a few training examples as part of the prompt during inference [17]. This has shifted some of the concerns around privacy of training data from training time to inference time. Furthermore, the consumer-facing nature and widespread accessibility [32, 74, 60, 93, 58] of LLMs have significantly amplified the scope of these privacy risks. What renders the privacy risks particularly potent is the general lack of awareness among users, leading to unwitting disclosure of sensitive information [11]. Consequently, certain countries, such as Italy [22], along with financial institutions [59, 102], government agencies [95, 75, 96], medical institutions [33] as well as companies, such as Samsung [90, 89], Amazon [4] and Apple [8], have prohibited the use of proprietary LLMs altogether, underscoring the significance of these privacy concerns.

![](/image/Preempt/2f2a7f3969ce3f5d87bbee14b235a35b25c32acb2a9cb0d956f697afbc45d231.jpg)  
Figure 1: Overview of Prϵϵmpt: Users begin with a one-time registration to set up configurations, which are used in all subsequent interactions. Users can then submit prompts to Prϵϵmpt and receive their sanitized versions, which are safe to be provided to the untrusted LLM. The LLM’s responses (to the sanitized prompts) can then be desanitized to recover high-utility responses.

Prior work on privacy-preserving LLMs [6, 66, 53, 85, 92, 72, 103], has primarily focused on mechanisms during training. Unfortunately, these training-time mechanisms can only protect the (pre)-training data: data provided as part of the prompt poses additional privacy risks that are not addressed by these mechanisms [34]. While recent research has begun to address the privacy of prompts, solutions based on homomorphic encryption and secure multiparty computation [49, 26, 54] are computationally expensive in practice, with state-of-the-art techniques taking over sixteen minutes for a single inference on BERT [82]. More efficient solutions either lack formal privacy guarantees [67, 106], require changes to current LLM APIs [70] or make impractical design choices [91, 61, 27] (see Sec. 6 for more details).

To this end, we make the following contributions. First, we introduce a cryptographically inspired notion of a prompt sanitizer that takes a prompt and transforms it in a way that protects sensitive tokens yet still preserves the ability of the LLM to make a useful prediction. We provide a formal analysis of both its privacy and utility. Second, we propose Prϵϵmpt2, a system that instantiates a prompt sanitizer. To the best of our knowledge, Prϵϵmpt is the first prompt sanitizer with formal privacy guarantees. As the first step in this direction, we focus on the sensitive information that can derived solely from the individual tokens. It is important to note that addressing this aspect is paramount as it poses the most immediate risk and represents a “low-hanging fruit” for potential adversaries. This is because an adversary can exploit the sensitive tokens (such as SSN, credit card number) independently, without needing to process or access additional context from the prompts. Moreover, in many settings, sensitive information is often restricted to structured (e.g., tabular) data that can be extracted as tokens—for instance, in financial Q/A tasks as evaluated in our experiments. The task of handling privacy risks stemming from the contextual linguistic semantics3 of the entire prompt [73, 15] is left as future work.

Prϵϵmpt operates on the assumption that sensitive tokens can be categorized into two types: (1) tokens for which the LLM’s response depends solely on their format. (e.g., SSN, credit card number), (2) tokens where LLM’s response depends on the specific numerical value itself (e.g., age, salary). Consequently, we propose encrypting the former using format-preserving encryption [12]: a type of property-preserving encryption scheme where the ciphertext and the plaintext have the same format. For example, the ciphertext of a 16-digit credit card number encrypted under a FPE scheme would also be a 16-digit number. Tokens of the second type are sanitized using differential privacy (DP) [37], which is the state-of-the-art technique for achieving data privacy. Specifically, we employ a relaxation of DP, called metric DP [23]. Metric DP protects pairs of inputs that are “similar” based on a distance metric, meaning that the sanitized token will remain similar to the original token. This approach maintains the relevance of the responses generated to the original prompt while providing meaningful privacy guarantees.

We demonstrate the practicality of Prϵϵmpt through empirical evaluation. Specifically, we evaluate four types of tasks: translation, retrieval augmented generation (RAG), long-context reading comprehension Q/A and multi-turn financial Q/A. We observe that Prϵϵmpt’s sanitization mechanism preserves the utility of responses across all tasks. For instance, the BLEU scores [84] for sanitized prompts are nearly identical compared to baseline unsanitized prompts for a German language translation task with GPT-4o. When prompted with Prϵϵmpt sanitized prompts, all RAG tasks achieved $100 \%$ accuracy. Prϵϵmpt is also quite successful in long-context and multi-turn conversation tasks. For example, responses based on Prϵϵmpt processed reference texts used in long-context Q/A has a similarity score of 0.934 compared to responses based on unsanitized text, outperforming a contemporary method [94] (PAPILLON) without any additional overheads.

# 2 Background

Notation. Let V be the vocabulary (tokens) of a language model and $\vee ^ { * }$ the set of possible strings over V (recall that a prompt and its response are strings over V). We represent a sequence of tokens $\bar { \pmb { \sigma } } \in \mathsf { V } ^ { * }$ with a boldface. Let $f$ be a LLM and $\pmb { \rho } \in \mathsf { V } ^ { * }$ be a prompt for it. A prompt is a sequence of tokens from V, i.e., $\pmb { \rho } = \langle \sigma _ { 1 } , \cdots , \sigma _ { n } \rangle , \sigma _ { i } \in \mathsf { V } , \forall i \in [ n ]$ . Let $\mathbb { P } ( \vee$ denote the space of all probability distribution over V.

# 2.1 Language Model

Definition 1. A language model $f$ is an auto-regressive model over a vocabulary V. It is a deterministic algorithm that takes a prompt $\pmb { \rho } \in V ^ { \ast }$ and tokens previously produced by the model $\sigma \in V ^ { \ast }$ as input, and outputs a probability distribution $p = f ( \pmb { \rho } , \pmb { \sigma } )$ for $p \in \mathbb { P } ( V )$ .

A language model’s response to a prompt $\rho$ is a random variable $\pmb { \sigma } \in \mathsf { V } ^ { * }$ that is defined algorithmically as follows. We begin with an empty sequence of tokens $\sigma = \langle \rangle$ . As long as the last token in $\pmb { \sigma }$ is not $\perp$ (which we can be viewed as ”end of sequence” (EOS) token), we sample a token $\sigma$ from the distribution $f ( \pmb { \rho } , \pmb { \sigma } )$ (using a decoding algorithm, such as multinomial sampling, or greedy sampling of the single most likely next token) and append it to $\sigma$ . The algorithm stops once a special token $\perp$ is emitted. Once the decoding algorithm is fixed, we can model $f$ as taking a prompt $p$ in $\bar { \mathsf { V } } ^ { \star }$ and outputting a string in $V ^ { \star }$ . In a slight abuse of notation, we will henceforth use $f ( \pmb { \rho } )$ to denote the response string of the LLM on the input prompt $\rho$ .

# 2.1.1 Tokens and Types

Given a sequence of tokens $\pmb { \sigma } \in \mathsf { V } ^ { \star }$ , a typed sequence is a 2-tuple $\pmb { \sigma } _ { \tau } = \langle ( \sigma _ { 1 } , \tau _ { 1 } ) , \cdot \cdot \cdot , ( \sigma _ { n } , \tau _ { n } ) \rangle$ , where $\tau _ { i } \in \mathsf { T }$ is the type of the substring $\sigma _ { i }$ of $\sigma$ (we assume $\pmb { \sigma } = \sigma _ { 1 } \cdot \sigma _ { 2 } \cdot \cdot \cdot \sigma _ { n } )$ ). Each type is associated with a domain. We also assume the existence of a type annotator.

Definition 2 (Type Annotator). A type annotator is a deterministic algorithm $\mathcal { M } _ { \tau } : V ^ { * } \mapsto ( V ^ { \star } \times T ) ^ { * }$ that inputs a prompt $\rho$ and outputs the corresponding typed sequence $\langle ( \sigma _ { 1 } , \tau _ { 1 } ) , \cdot \cdot \cdot \bar { , } ( \sigma _ { n } , \tau _ { n } ) \rangle$ .

For example, consider the following prompt $\rho$ : “Kaiser Soze is 50 years old and earns 500,000 per year. What is his ideal retirement plan?” $\scriptstyle { \mathcal { M } } _ { \tau } ( \rho )$ is given as follows: “(Kaiser Soze, [Name]) is (50, [Age]) years old and earns (500,000 , [Salary]) per year. What is his ideal retirement plan?”, where [Name], [Age], [Salary] are types of the tokens that precede it. For the ease of notation, here we only annotate tokens with sensitive types, i.e., all other non-annotated tokens have type $\perp$ (which denotes non-sensitive token). Note that type annotation is context dependent. For example, consider the following two prompts: $\rho _ { 1 } =$ $\rho _ { 1 } \mathrm { = } \mathbf { \dot { \Omega } } \mathbf { M } \mathbf { y }$ age is 53 years.” and $\rho _ { 2 } = { } ^ { \ast } \mathrm { { I } }$ stay at 53 Broadway Street.” The same token 53 has two different types in the two prompts: type Age and type Street Number in $\rho _ { 1 }$ and $\rho _ { 2 }$ , respectively.

# 3 Prompt Sanitizer

Given an input prompt $\rho$ , a prompt sanitizer (denoted by PS) transforms the entire prompt to a sanitized one $\hat { \pmb \rho }$ with the goal of protecting the sensitive tokens contained in $\rho$ . It is formally defined as follows:

Definition 3 (Prompt Sanitizer). A prompt sanitizer $P S = \langle S , \mathcal { M } _ { \tau } , E , D \rangle$ is a tuple of the following algorithms:

• Setup (S). The setup algorithm takes no input and outputs a secret key, as $K  S$ .   
• Type Annotator $( \mathcal { M } _ { \tau } )$ . The type annotator inputs a prompt (token sequence) $\pmb { \rho } \in V ^ { * }$ and outputs the corresponding type-annotated token sequence as $\pmb { \rho } _ { \tau } \gets \mathcal { M } _ { \tau } ( \pmb { \rho } )$ (as defined in Def. 2).

• Sanitization $( E )$ . The sanitization algorithm takes as input the secret key $\boldsymbol { \kappa }$ and a type-annotated token sequence $\pmb { \rho } _ { \tau } \in ( V ^ { \star } \times T ) ^ { * }$ . It outputs a token sequence $\hat { \pmb { \rho } } \in V ^ { | \pmb { \rho } _ { \tau } | }$ , as $\hat { \pmb { \rho } } \gets E ( K , \pmb { \rho } _ { \tau } )$ .   
• Desanitization $( D )$ . Desanitization takes a string (token sequence) $\hat { \mathbf { \Omega } } ^ { \hat { \mathbf { v } } } \in \mathbf { \Omega } ^ { V ^ { \ast } }$ and processes it with the goal of reversing the effect of the sanitization algorithm, using the secret key $\kappa$ This is represented as $\pmb { v } \gets D ( K , \hat { \pmb { v } } )$ with υ ∈ V|υˆ|. $\boldsymbol { v } \in \boldsymbol { V } ^ { | \hat { v } | }$

Given a prompt $\rho$ , the typical workflow of PS proceeds as follows:

(1) type annotate the prompt to obtain $\pmb { \rho } _ { \tau } = \mathcal { M } _ { \tau } ( \pmb { \rho } )$   
(2) sanitize the type annotated prompt using the secret key $\mathsf { K }$ as $\hat { \pmb { \rho } } = \mathsf { E } ( \mathsf { K } , \pmb { \rho } _ { \tau } )$   
(3) obtain the LLM’s response on the sanitized prompt as $\hat { \boldsymbol { v } } = f ( \hat { \boldsymbol { \rho } } )$   
(4) desanitize the response to obtain $\pmb { v } = \pmb { \mathrm { D } } ( \pmb { \mathrm { K } } , \bar { \hat { \pmb { v } } } )$

In the above workflow, the desanitization algorithm restores information about the original prompt $\rho$ in its output, $_ w$ In the special case where we run the desanitization algorithm directly on the sanitized prompt $\hat { \pmb \rho }$ (which can be useful for instance if the PS is used to store a set of sensitive prompts on an untrusted platform for later use), we ideally expect $v = \rho$ .

We require that the sanitization and desanitization algorithms are type preserving, which means that if $\rho =$ $\langle \sigma _ { 1 } , \cdots , \sigma _ { n } \rangle$ and $\pmb { \rho } _ { \tau } = \langle ( \sigma _ { 1 } , \tau _ { 1 } ) , \cdot \cdot \cdot , ( \sigma _ { n } , \tau _ { n } ) \rangle  \mathcal { M } _ { \tau } ( \pmb { \rho } )$ and $\hat { \pmb { \rho } } \gets \mathsf { E } ( \mathsf { K } , \pmb { \rho } _ { \tau } )$ and $\langle ( \sigma _ { 1 } ^ { \prime } , \tau _ { 1 } ^ { \prime } ) , \cdot \cdot \cdot , ( \sigma _ { n } ^ { \prime } , \tau _ { n } ^ { \prime } ) \rangle $ $\mathcal { M } _ { \tau } ( \hat { \pmb { \rho } } )$ then it must be that $( \tau _ { 1 } , \cdot \cdot \cdot , \tau _ { n } ) = ( \tau _ { 1 } ^ { \prime } , \cdot \cdot \cdot , \tau _ { n } ^ { \prime } )$ .

# 3.1 Privacy Guarantee

The privacy game, denoted as $\mathbf { G } _ { \mathsf { P S } , \mathcal { L } } ^ { \mathrm { p p } }$ , is designed to capture an adversary’s ability to distinguish between the sanitized outputs of two different prompts. In the game if the adversary picks two prompts that have a very different structure (e.g. different type or number of tokens), then the adversary can trivially distinguish between the corresponding sanitized prompts. To rule out pathological cases, we restrict the adversary to selecting two prompts with a “similar structure”, formalized via a leakage function. Different instantiations of the leakage function lead to different instantiations of the game.

The game is defined as follows:

INITIALIZE:

1: $\mathsf { K } \gets \mathsf { S } ($   
2: $b \gets \{ 0 , 1 \} \triangleright$ Select a random bit   
$\mathrm { S A N I T I Z E } ( \rho _ { 0 } , \rho _ { 1 } ) \colon$ ▷ Adversary selects two prompts   
3: $\overline { { L _ { 0 }  \mathcal { L } ( \pmb { \rho } _ { 0 } ) ; L _ { 1 } } }  \mathcal { L } ( \pmb { \rho } _ { 1 } )$   
$\triangleright \mathcal { L }$ is the leakage function associated with PS   
4: if $L _ { 0 } \neq L _ { 1 }$ then return $\perp$   
$\vartriangleright$ Only prompt pairs with the same leakage are valid   
5: $\hat { \pmb { \rho } } _ { 0 } \gets \mathsf { E } ( \mathsf { K } , \bar { \mathcal { M } } _ { \tau } ( \pmb { \rho } _ { 0 } ) ) ; \hat { \pmb { \rho } } _ { 1 } \gets \mathsf { E } ( \mathsf { K } , \mathcal { M } _ { \tau } ( \bar { \pmb { \rho } } _ { 1 } ) )$   
6: return $\hat { \pmb { \rho } } _ { b }$   
$\vartriangleright$ Return one of the sanitized prompts chosen at random $\mathrm { F I N A L I Z E } ( b ^ { \prime } )$ :   
7: return $\overline { { [ b ^ { \prime } = b } } ]$

$\vartriangleright { \boldsymbol { b } } ^ { \prime }$ is the adversary’s guess for $b$

We denote an adversary by $\mathcal { A }$ . We model the information leakage from the sanitized prompts through a leakage function, $\mathcal { L }$ . In particular, the leakage function $\mathcal { L }$ of a prompt sanitizer takes as input a prompt $\rho$ and captures all the information about sensitive tokens that is leaked by $\hat { \pmb { \rho } } = \sf E ( \pmb { \rho } , \sf K )$ , given a key K. In the above game, an adversary $\mathcal { A }$ aims to distinguish between the sanitized prompts of $\rho _ { 0 }$ and $\pmb { \rho } _ { 1 }$ based solely on the sanitized output and the leakage allowed by $\mathcal { L }$ . The adversary is said to win the game if $\dot { b } ^ { \prime } = b$ and their advantage is formally defined as:

$$
\mathbf {A d v} _ {\mathrm {P S}, \mathcal {L}} ^ {\mathrm {p p}} (\mathcal {A}) = 2 \Pr \left[ \mathbf {G} _ {\mathrm {P S}, \mathcal {L}} ^ {\mathrm {p p}} (\mathcal {A}) = 1 \right] - 1.
$$

Intuitively, the game implies that even after observing a sanitized prompt, an adversary should not be able to reliably differentiate between two prompts with the same leakage. The definition of the leakage function, $\mathcal { L }$ , is crucial and depends on the underlying sanitizer E. For example, if $\mathsf { E }$ sanitizes a token by redaction, for prompt $\rho = \mathrm { ^ { * } M y }$ age is $2 6 ^ { \circ }$ , the leakage function outputs all the non-sensitive tokens, i.e., ${ \mathcal { L } } ( \rho ) = { \mathfrak { s } } _ { \mathbf { M } \mathbf { y } }$ age is [ ]”—this represents the minimal possible leakage as redaction is the strongest sanitization mechanism. Alternatively, if E encrypts sensitive tokens, $\mathcal { L }$

might reveal the length of these tokens to $\mathcal { A }$ . Note that leakage function is a standard notion in cryptography [40]. For instance, the leakage function for order-preserving encryption [69] is essentially the numerical ordering of the input dataset.

The restriction in the above game, requiring the pair of prompts to have the same leakage, aligns with standard notions in game-based cryptographic security definitions. For instance, this is similar to the definition of security in orderpreserving encryption (IND-FA-OCPA [69]), where the adversary is restricted to selecting pairs of data sequences that maintain the same order.

# 3.2 Utility Guarantee

Let $\mathcal { Q } : \mathsf { V } ^ { * } \times \mathsf { V } ^ { * } \mapsto R _ { \mathcal { Q } }$ be a quality oracle that evaluates the quality of a candidate response $_ w$ for a prompt $\rho$ . Specifically, $\mathcal { Q } ( \pmb { \rho } , \pmb { v } )$ is a measure of the response’s goodness. Such a quality oracle has been used in prior work on LLMs [105].

Definition 4. A prompt sanitizer PS satisfies $( \alpha , \beta )$ utility for a given prompt $\pmb { \rho } \in V ^ { \ast }$ ,

$$
\alpha = \mathbb {E} _ {f} \left[ Q (\boldsymbol {\rho}, f (\boldsymbol {\rho})) \right] \tag {1}
$$

$$
\beta = \mathbb {E} _ {f, P S} \left[ Q (\boldsymbol {\rho}, D (K, f (\hat {\boldsymbol {\rho}})) \right], \hat {\boldsymbol {\rho}} = E (K, \mathcal {M} _ {\tau} (\boldsymbol {\rho})) \tag {2}
$$

where the randomness is defined over both the LLM, f, and PS.

The utility of the prompt sanitizer PS is evaluated by comparing the quality of the original response $f ( \pmb { \rho } )$ with the one obtained through the PS pipeline. The above definition has two key characteristics. First, the utility is defined w.r.t to a specific prompt, as response quality can vary significantly across different prompts. For example, consider the following prompt: $\rho = { } ^ { \ast } M y$ age is 46. What is the average age of the population of New York?” Here, a highquality LLM’s response should be invariant to the sensitive token $( [ A g e ] )$ in the prompt. This means that even after sanitization, we should be able to retrieve a correct and relevant response. On the other hand, for a conversational prompt used in a LLM-based chatbot to seek medical advice, the quality of the responses could vary significantly based on the specifics of the sanitization and desanitization algorithms of PS. Note that the quality oracle $Q$ can take various forms based on the type of the prompt. For instance, it might be a human evaluator who assigns a quality score, or it could be a predefined analytical expression in case the prompt has some special structures. Second, utility is defined as an expectation, since in general both the LLM f and the prompt sanitizer PS, are probabilistic. Note that when the distribution of $f ( \rho )$ matches the distribution of $\mathsf { D } ( \mathsf { K } , f ( \hat { \pmb { \rho } } ) )$ , this represents the strictest form of utility. If $R _ { Q }$ is a metric space with a distance metric $d _ { Q }$ , we can quantitatively measure the mean degradation in the quality of the response as $d _ { Q } ( \alpha , \beta )$ .

# 4 Prϵϵmpt System Description

This section introduces Prϵϵmpt: a system that instantiates a sanitizer for prompts. First, we describe the primitives (FPE and mDP) in subsection 4.1. Next, two sections describe our threat model and design goals. Our system is described in subsection 4.4. We conclude the section with privacy and utility analysis. Our last subsection discusses other “strawman” solutions and why they don’t address our threat model and goals.

# 4.1 Building Blocks

We start by describing the building blocks which will be used to sanitize the sensitive tokens.

# 4.1.1 Format-Preserving Encryption (FPE)

Under a format preserving encryption (FPE) scheme, the plaintext and the ciphertext have the same format, that is, FPE ensures that the encrypted output is structurally similar to the original input, including properties such as length, character set, or format. This property allows applications to process ciphertexts and plaintexts in the same way. This backward compatibility makes FPE a popular tool for secure data analytics in practice. For instance, the ciphertext of a 16-digit credit card number encrypted under a FPE scheme would also be a 16-digit number4. As concrete examples, a plaintext Social Security number such as 055-46-6168 might be transformed into the ciphertext 569-83-4469, while an

IP address like 76.217.83.75 could be encrypted as 97.381.64.35. Intuitively, FPE shuffles or re-encodes values within the space of all valid values of the same type. Without the decryption key, the ciphertext looks indistinguishable from any legitimate value of that format, effectively hiding the original data while remaining compatible with systems that expect specific formats.

Definition 5 (Format Preserving Encryption (FPE)). A format preserving encryption scheme is a tuple $\varepsilon \quad =$ $\langle G _ { \mathcal { F } } , E _ { \mathcal { F } } , D _ { \mathcal { F } } \rangle$ of polynomial time algorithms:

• Key Generation $( G _ { \mathcal { F } } )$ . The key generation algorithm is probabilistic polynomial time algorithm that takes as input a security parameter κ and outputs a secret key K as $K \gets G _ { \mathcal { F } } ( 1 ^ { \kappa } )$ .   
• Encryption $( E _ { \mathcal { F } } ) ^ { 5 }$ . The encryption algorithm is deterministic polynomial time algorithm that takes as input a secret key $\kappa ,$ a plaintext $x \in \mathcal { M }$ , and a format $N \in \mathcal N$ and outputs a ciphertext $y \in \mathcal { M }$ as $y  E _ { \mathcal { F } } ( K , N , x )$   
• Decryption $( D _ { \mathcal { F } } )$ . The decryption algorithm is deterministic polynomial time algorithm that recovers the plaintext as $x  D _ { \mathcal { F } } ( K , N , y )$ .

Typically, the format of a plaintext is described as a finite set N over which the encryption function induces a permutation. For example, with SSNs this is the set of all nine-decimal-digit numbers.

# 4.1.2 Metric Local Differential Privacy (mLDP)

Differential privacy (DP) is a quantifiable measure of the stability of the output of a randomized mechanism to changes to its input. As a direct consequence of our threat model (Sec. 4.2), we work with the local model of DP (LDP) where each data point is individually randomized. Metric local differential privacy (mLDP) [23, 3, 88, 56] is a generalization of LDP which allows heterogenous guarantees for a pair of inputs based on a distance metric $d ( \cdot )$ defined over the input space.

Definition 6 (Metric Local Differential Privacy (mLDP) [23]). A randomized algorithm $\mathcal { M } : \mathcal { X }  \mathcal { Y }$ is ϵ-mLDP for a given metric $d : \mathcal { X } \times \mathcal { X } \mapsto \mathbb { Z } _ { \ge 0 }$ if for any pair of private values $x , x ^ { \prime } \in { \mathcal { X } }$ and any subset of output, $\mathcal { O } \subseteq \mathcal { V }$

$$
\Pr \left[ \mathcal {M} (x) \in \mathcal {O} \right] \leq e ^ {\epsilon d \left(x, x ^ {\prime}\right)} \cdot \Pr \left[ \mathcal {M} \left(x ^ {\prime}\right) \in \mathcal {O} \right] \tag {3}
$$

mLDP uses the distance between a pair of values to customize heterogeneous (different levels of) privacy guarantees for different pairs of private values. In particular, the privacy guarantee degrades linearly with the distance between a pair of data points; that is, only data points that are “close” to each other should be indistinguishable. Still, mLDP captures the privacy semantics of many real-world scenarios and is well suited to settings where releasing approximate information is acceptable. For example, it is often sufficient to reveal a coarse location, such as a city block, rather than exact GPS coordinates. Similarly, sharing an income range (e.g., $\$ 60 K -480 K )$ can preserve utility without exposing precise figures. Alg. 3 in App. .1, outlines a mechanism for achieving $\epsilon$ -mLDP for the $\ell _ { 1 }$ distance using a variant of the exponential mechanism [37].

Theorem 1. Mechanism $\mathcal { M } _ { \epsilon }$ satisfies ϵ-mLDP for the $\ell _ { 1 }$ distance.

The proof of the theorem is standard and appears in the appendix. However, we next justify why $\mathcal { M } _ { \epsilon }$ is an appropriate notion for our context. An input is more likely to be mapped to one which is close to it, which we formalize this using the following two properties.

Property 1.

$$
\Pr \left[ \mathcal {M} _ {\epsilon} (x, \epsilon , [ k ]) = x \right] > \Pr \left[ \mathcal {M} _ {\epsilon} (x, \epsilon , [ k ]) = y \right], \forall y \in [ k ]
$$

Property 2.

$$
\left| y _ {1} - x \right| <   \left| y _ {2} - x \right| \Longleftrightarrow
$$

$$
\Pr \left[ \mathcal {M} _ {\epsilon} (x, \epsilon , [ k ]) = y _ {1} \right] > \Pr \left[ \mathcal {M} _ {\epsilon} (x, \epsilon , [ k ]) = y _ {2} \right],
$$

$$
\forall y _ {1}, y _ {2} \in [ k ]
$$

# 4.2 Threat Model

Prϵϵmpt runs as an application on a user’s (trusted) local device. Additionally, Prϵϵmpt can support multiple users: envision it as an application maintained at the level of an organization and available to all of its employees. The user

inputs a string $( \mathsf { V } ^ { * } )$ to Prϵϵmpt and obtains a transformed string. Every such interaction constitutes a separate session. In particular, consider the following chain of events. An user $U$ submits a prompt $\rho$ to Prϵϵmpt and obtains a sanitized version of it $\hat { \pmb \rho }$ . Next, they obtain a response $\hat { v }$ from an LLM on $\hat { \pmb \rho }$ and again uses Prϵϵmpt to desanitize it into $\textbf { \em w }$ . This interaction constitutes two separates Prϵϵmpt sessions: one for the $\rho  { \hat { \boldsymbol { \rho } } }$ transformation and the other for the $\hat { v } \to v$ transformation. The LLM is an untrusted third-party application which represents the adversary (Fig. 1).

In Prϵϵmpt, we focus on tokens where the sensitive information can be derived solely from the individual token, with no extra context. Examples of such token types include SSN, credit card number, license number, age, money, A/C number, zipcode. Privacy issues stemming from the linguistic context of the prompts (e.g. a prompt indicating the users’ mental health details) are beyond Prϵϵmpt’s scope (see App. .9 for more discussion).

# 4.3 Design Goals

Prϵϵmpt has the following design goals.

• Formal Guarantees. Prϵϵmpt should be able to provide a formal privacy guarantee on the sanitized prompts.   
• High Utility. The responses based on sanitized prompts should be “close” to the responses based on the original prompt.   
• Stateless. Finally, the sanitization and desanitization process should be stateless, i.e., Prϵϵmpt should not retain information (state) from any prior session. This design choice offers dual advantages. Firstly, storing sensitive information derived from users’ prompts/responses post-session termination would violate privacy and contravene legal frameworks, such as the EU’s GDPR [47] and California’s CCPA [18]. Additionally, these regulations grant individuals the Right to Deletion, allowing data owners to retract authorization previously granted for the use of their personal data. A stateful solution hinders the Right to Deletion and desanitization, while a stateless one offers flexibility and storage efficiency. For example, consider these two user action sequences:

$$
\begin{array}{l} A _ {1} = \left\langle \text {S a n i t i z e} \rho_ {1}; \text {D e s a n i t i z e} \hat {v} _ {1}; \text {S a n i t i z e} \rho_ {2}; \right. \\ \left. \text {D e s a n i t i z e} \hat {v} _ {2}; \text {S a n i t i z e} \rho_ {3}; \text {D e s a n i t i z e} \hat {v} _ {3} \right\rangle \\ A _ {2} = \langle \text {S a n i t i z e} \rho_ {1}; \text {S a n i t i z e} \rho_ {2}; \text {D e s a n i t i z e} \hat {v} _ {2}, \\ \text {S a n i t i z e} \rho_ {3}, \text {D e s a n i t i z e} \hat {\boldsymbol {v}} _ {1}, \text {D e s a n i t i z e} \hat {\boldsymbol {v}} _ {3} \rangle . \\ \end{array}
$$

Without perpetual retention of state information, a stateful solution restricts a user to a specific action sequence of sanitizing and desanitizing in order (such as, $A _ { 1 }$ ). Moreover, multiple desanitization of the same string cannot be supported without perpetual storage of the state information. The issue is exacerbated with multiple users as a stateful solution entails storing separate state information for each user. In contrast, a stateless solution provides the flexibility of supporting arbitrary sequences of user actions (such as, $A _ { 2 }$ ).

Note that while Prϵϵmpt is stateless, conversation with the LLM can be stateful – the LLM is free to maintain a history of all (sanitized) prompts to better respond to user queries. We illustrate this experimentally in Sec. 5.

# 4.4 System Modules

Prϵϵmpt supports three types of sessions, namely, User Registration, Sanitization and Desanitization, which is taken care of by the following modules.

Configuration Manager. The configuration manager module of Prϵϵmpt generates a secret key ${ \sf K } _ { U } \to { \sf G } ( 1 ^ { \kappa } )$ for a given security parameter for an user $U$ at the time of the registration for a FPE scheme $\mathcal { E }$ . Subsequently, for any session involving user $U$ , this module initializes all instances of the FPE scheme with the key $\mathsf { K } _ { U }$ . Additionally, during registration, user $U$ specifies the privacy parameter $\epsilon$ for $\mathcal { M } _ { \epsilon }$ , which is treated as the privacy budget for each individual sanitization session. The module also initializes the data domain (equivalently, format in the case of FPE) for each sensitive token type. The domains can either be predefined or computed based on some user-provided information. Lastly, various parameters (e.g. format and privacy parameter) can be dependent on the type $\tau$ .

Sanitizer. Recall that Prϵϵmpt only sanitizes sensitive tokens that are alphanumeric or numeric (see Sec. 4.2). To this end, Prϵϵmpt assumes that such sensitive tokens fall into two distinct categories:

• Category $I \left( \tau _ { \perp } \right)$ . These tokens are characterized by the fact that the LLM’s response depends solely on their format. Examples of tokens in this category include names, Social Security Numbers (SSN), credit card numbers, Taxpayer Identification Numbers (TIN), passport numbers, bank account numbers, driver’s license numbers, phone numbers, license numbers, and IP addresses. We provide empirical evidence of this assumption in Sec. 5.

• Category $I I \left( \tau _ { \perp \perp } \right)$ . This category encompasses tokens where the LLM’s response hinges on the specific numerical value itself, such as age, medical records6, etc. That is, the LLM performs specific computations based on the values of these tokens.

Algorithm 1 Prϵϵmpt: Sanitization   
Input: $\rho$ - Input prompt; $K_U$ - Sanitization key; $\epsilon$ - Total budget  
Output: $\hat{\rho}$ - Sanitized prompt;  
1: $\rho' = \langle \rangle$ 2: $\rho_{\tau} \gets \mathcal{M}_{\tau}(\rho) \triangleright \mathcal{M}_{\tau}$ is instantiated with a named-entity recognizer  
3: $(\psi, t) \gets \mathcal{M}_{\mathrm{Pre}}(\rho, \rho_{\tau}) \triangleright \Psi$ is a helper string encoding some extra information about the type of tokens $\triangleright$ $t$ is the number of tokens in $\rho_{\tau}$ with type $\tau_{II}$ 4: for $(\sigma, \tau) \in \rho_{\tau}$ 5: if $(\tau \neq \bot)$ 6: if $(\tau == \tau_{\mathbb{I}})$ 7: $\hat{\sigma} = E_{\mathcal{F}}(K_U, N_{\tau}, \sigma) \triangleright N_{\tau}$ is the format of $\sigma$ 8: else  
9: $\hat{\sigma} = \mathcal{M}_{\epsilon}(\sigma, \frac{\epsilon}{t}, k_{\tau}) \triangleright [k_{\tau}]$ is the domain of $\sigma$ 10: end if  
11: else  
12: $\hat{\sigma} = \sigma$ 13: end if  
14: $\rho'$ .append(\hat{\sigma})  
15: end for  
16: $\hat{\rho} \gets \mathcal{M}_{\mathrm{Post}}(\rho', \Psi) \triangleright$ Performs some post-processing on the sanitized tokens  
17: return $\hat{\rho}$

A prompt is sanitized as follows. We first perform type annotation of the different tokens via $\mathcal { M } _ { \tau }$ . In addition to annotating the type of a token, $\mathcal { M } _ { \tau }$ also indicates its category. For Prϵϵmpt, we instantiate $\mathcal { M } _ { \tau }$ with a named-entity recognizer (NER). Next, Prϵϵmpt uses a pre-processor $\mathcal { M } _ { \sf P r e }$ that takes $( \rho , \rho _ { \tau } )$ as input and computes two things; 1) it determines the number of tokens belonging to the second category, denoted as t, 2) it computes a helper string $\Psi$ to encode additional information about token types and provide flexibility during sanitization. Specifically, $\Psi$ captures functional dependencies between the tokens. We present examples involving the helper string in Sec. 4.5 and App. .7.

In Prϵϵmpt, each sensitive token is sanitized individually. In particular, all tokens of the first category are sanitized using FPE with the user specific secret key $\mathsf { K } _ { U }$ . On the other hand, all tokens of the second category are sanitized to satisfy $\frac { \epsilon } { t }$ -mLDP using $\mathcal { M } _ { \epsilon }$ , where $\epsilon$ is the privacy parameter for the standard DP guarantee and $t$ is the maximum distance between protected values. No operation is performed on tokens with non-sensitive types $\tau = \perp$ ). Next, all sanitized tokens are concatenated and passed to a post-processor $\mathcal { M } _ { \sf P o s t }$ . The $\mathcal { M } _ { \sf P o s t }$ enforces the functional dependencies encoded in $\Psi$ . Furthermore, in Prϵϵmpt only the determinant is perturbed, and the sanitized versions of the dependent tokens are derived from this noisy encoding. If $\Psi$ is empty (i.e. not functional dependencies are provided), then each token is handled independently and no functional dependencies are enforced, which can adversely affect utility. The full sanitization mechanism is outlined in Algorithm 1. Steps 3-17 in Alg. 1 instantiate the sanitization algorithm E of the prompt sanitizer (Def. 3).

Desanitizer. Desanitization (Alg. 2) begins with the same type annotator. All sensitive tokens of category I can be desanitized using the decryption algorithm of the FPE scheme. However, tokens sanitized with $\mathcal { M } _ { \epsilon }$ cannot be desanitized without retaining additional state information and are hence, left untouched by default. Steps 3-11 in Algorithm 2 correspond to the desanitization algorithm D of the prompt sanitizer (Def. 3).

One drawback of this approach is that tokens from the first category that did not appear in the original prompt (and consequently were never sanitized) might also undergo desanitization. Users can mitigate this by providing the original prompt $\rho$ as auxiliary information. In this scenario, Prϵϵmpt will exclusively desanitize tokens that appeared in the prompt. Note that the only thing required to desanitize is the secret key $\mathsf { K } _ { U }$ : Prϵϵmpt does not store any sensitive information post the termination of a session thereby making our solution stateless.

Algorithm 2 Prϵϵmpt: Desanitization   
Input: $\hat{v}$ - Input sanitized response; $K_U$ - Sanitization key; Output: $\pmb{v}$ - Desanitized response;  
1: $\pmb{v} = \langle \rangle$ 2: $\hat{\pmb{v}}_{\tau} \gets \mathcal{M}_{\tau}(\hat{\pmb{v}}) \triangleright \mathcal{M}_{\tau}$ is instantiated with a named-entity recognizer  
3: for $(\sigma, \tau) \in \hat{\pmb{v}}_{\tau}$ 4: if $(\tau == \tau_I)$ 5: $\sigma = D_{\mathcal{F}}(K_U, N_{\tau}, \sigma) \triangleright N_{\tau}$ is the format of $\sigma$ 6: else  
7: $\sigma = \hat{\sigma}$ 8: end if  
9: $\pmb{v}$ .append(\sigma)  
10: end for  
11: return $\pmb{v}$

# 4.5 Setting up Parameters

In this section, we provide guidelines on how to choose the parameters for Prϵϵmpt.

Setting up ϵ. If a user desires a privacy parameter of $\epsilon$ for the standard DP guarantee and wishes to protect values that differ by at most distance l, then use $\epsilon ^ { \prime }$ -mLDP with $\begin{array} { r } { \epsilon ^ { \prime } = \frac { \epsilon } { l } } \end{array}$ . Any $\epsilon$ -mLDP protocol is $\epsilon \cdot l _ { m a x }$ -DP where the distance between any pair of inputs is at most $l _ { m a x }$ .

Using the helper string $\Psi$ . The helper string $\Psi$ encodes auxiliary knowledge that captures functional dependencies among sensitive tokens. These dependencies typically fall into two categories: (1) Common knowledge, such as mathematical or definitional identities (e.g., Annual Salary = 12 × Monthly Salary), and (2) Domain-specific knowledge, such as medical or financial formulas (e.g., $\begin{array} { r } { B M I = \frac { \dot { W } e i g h t } { H e i g h t ^ { 2 } } . } \end{array}$ WeightHeight2 . )

For common knowledge, the dependencies can be stored in a knowledge base and appended directly to the prompt to aid reasoning or consistency. Since these are standardized and widely accepted relationships, they can be programmatically injected with little ambiguity.

Handling domain-specific dependencies is more complex. One possible approach is to use a local LLM to infer dependencies between sensitive attributes identified by NER, producing structured representations of causal or computational links. These dependencies can then be modeled as a directed acyclic graph (DAG), where each node corresponds to a sensitive attribute and edges represent dependencies (e.g., computation or inference). The root nodes represent the base sensitive values and are directly noised using mLDP. These values are then propagated along the DAG via the encoded dependencies, ensuring that related fields (such as income and tax, or weight and BMI) are sanitized consistently.

# 4.6 Privacy and Utility Analysis

Privacy Analysis. The formal privacy guarantee of Prϵϵmpt is given as follows:

Theogame Let S be the set of all token pairs of type. Then, for Prϵϵmpt we have: $\tau _ { T , I }$ that are different in the prompt pairs $( \rho _ { 0 } , \rho _ { 1 } )$ in the privacy $\mathbf { G } _ { P S , \mathcal { L } } ^ { \mathrm { p p } }$

$$
\mathbf {A d v} _ {P r \epsilon \text {e m p t}, \mathcal {L}} ^ {\mathrm {p p}} (\mathcal {A}) \leq e ^ {l \epsilon} + \operatorname {n e g l} (\kappa) \tag {4}
$$

where $l = \operatorname* { m a x } _ { ( \sigma _ { 0 } , \sigma _ { 1 } ) \in S } \{ | \sigma _ { 0 } - \sigma _ { 1 } | \}$ and κ is the security parameter of the underlying FPE scheme.

Proof Sketch. First, we compute the adversary’s advantage in Prϵϵmpt when the two prompts $( \rho _ { 0 } , \rho _ { 1 } )$ differ by only a single token, denoted as AdvppPrϵϵ $\bar { \mathbf { A d v } } _ { \mathrm { P r } \epsilon \epsilon \mathrm { m p t } , \mathcal { L } = 1 } ^ { \mathrm { p p } } ( \mathcal { \bar { A } } )$ . Next, using the classic hybrid argument [78], we establish an upper bound on the adversary’s advantage in the general case, expressedby just a single token. Finally, Eq. 4 can be derived by substituting $\mathbf { A d v } _ { \mathrm { P r } \epsilon \epsilon \mathrm { m p t } , \mathcal { L } = 1 } ^ { \mathrm { p p } } ( \mathcal { A } )$ ntage when the prompts differ into this result. The full proof

# Practical Privacy Considerations.

Error due to NER. Prϵϵmpt’s privacy guarantee is cryptographic and orthogonal to NER. Specifically, Prϵϵmpt uses NER as a black-box and the above theorem aligns with the standard $\mathcal { F } _ { \mathrm { N E R } }$ -hybrid model of security where $\mathcal { F } _ { \mathrm { N E R } }$ is an ideal functionality for NER [79]. Importantly, the performance of NER should not be conflated with the efficacy

of the sanitization scheme. While the practical performance depends on properly identifying sensitive tokens, this is inherent to our task. As NER continues to improve, so will Prϵϵmpt’s practical performance without any modifications to the design. Additionally, domain-specific pattern matching with regular expressions can achieve high performance for structured data.

Nevertheless, we provide the following result that formalizThe main idea is to model errors within the leakage function $\mathcal { L }$ how to analyze privof our privacy game $\dot { \mathbf { G } } _ { \mathsf { P S } , \mathcal { L } } ^ { \mathrm { p p } }$ he presence of NER errors.. If the false negative rate of NER  the two prompts ρ0 and ρ1 for the corresponding privacy game GppPS,LNER , we proceed as follows: we start with the the NER is $\lambda$ , we define a leakage function $\rho _ { 0 }$ $\pmb { \rho } _ { 1 }$ $\mathcal { L } _ { \mathrm { N E R } }$ that additionally leaks up to $\mathbf { G } _ { \mathsf { P S } , \mathcal { L } _ { \mathrm { N E R } } } ^ { \mathrm { p p } }$ $\lambda \%$ of the sensitive tokens. To construct original prompt pair as in the unmodified game $\mathbf { G } _ { \mathsf { P S } , \mathcal { L } } ^ { \mathrm { p p } }$ , and then modify $\pmb { \rho } _ { 1 }$ by replacing $\lambda \%$ of its sensitive tokens with the corresponding tokens from $\rho _ { 0 }$ . In other words, this construction models the scenario where the adversary gains access to a fraction of sensitive tokens that were missed by the NER. Prϵϵmpt then protects the rest of the sensitive tokens as:

Theogame et S be the set of all token pairs of type. Then, for Prϵϵmpt we have: $\tau _ { T , I }$ that are different in the prompt pairs $( \rho _ { 0 } , \rho _ { 1 } )$ in the privacy ${ \bf G } _ { P S , \mathcal { L } _ { N E R } } ^ { \mathrm { p p } }$

$$
\mathbf {A d v} _ {P r \epsilon m p t, \mathcal {L} _ {N E R}} ^ {\mathrm {p p}} (\mathcal {A}) \leq e ^ {l \epsilon} + n e g l (\kappa) \tag {5}
$$

where $l = \operatorname* { m a x } _ { ( \sigma _ { 0 } , \sigma _ { 1 } ) \in S } \{ | \sigma _ { 0 } - \sigma _ { 1 } | \}$ and $\kappa$ is the security parameter of the underlying FPE scheme.

The proof of the above theorem is in App. .11.

Correlated Tokens. To mitigate correlation attacks, Prϵϵmpt adopts a conservative approach by dividing the privacy budget equally among all tokens of type $\tau _ { \mathrm { I I } }$ . This ensures that, via composition, the total privacy loss remains bounded by $\epsilon$ . However, leveraging the helper string $\Psi$ can yield a better privacy-utility tradeoff. For example, in the prompt, “My age is $X$ , I was born in $Y$ . I am X years old.”, $[ A g e : X ]$ , $\mathbf { \tilde { \mu } } [ Y e a r : Y ]$ and $[ A g e : X ]$ are the sensitive tokens. By default, Prϵϵmpt distributes the privacy budget equally $( \epsilon / 3 )$ among all type $\tau _ { \ I \ I }$ tokens, however, the helper string $\Psi$ can indicate that $X$ and $Y$ represent the same ground-truth and that $X$ is repeated. Using $\Psi$ , Prϵϵmpt applies $\epsilon$ -mLDP to the first occurrence of $X$ , yielding ${ \hat { X } } = 2 5$ (suppose). Prϵϵmpt then derives the corresponding $\hat { Y } \ : = \ : 2 0 0 0$ by post-processing and reuses $\hat { X }$ for the second occurrence of age. This incurs no additional privacy loss due to the post-processing immunity of mLDP [38]. Thus, the resulting sanitized prompt is given by: “My age is 25, I was born in 2000. I am 25 years old.”. We present additional illustrative examples in App. .7.

# Utility Analysis. We analyze Prϵϵmpt’s utility below.

Prompts with Perfect Utility. Recall that, for assessing utility, we compare the responses of the LLM to the original prompt $\rho$ and the sanitized prompt $\hat { \pmb \rho }$ produced by Prϵϵmpt. For many practically useful prompts, the response of the LLM remains the same for both $( \rho , \hat { \rho } )$ except for the substitution of the sensitive tokens $\sigma \in \rho$ with their sanitized counterparts $\hat { \sigma }$ . In other words, the sanitized response $\hat { v }$ generated from $\hat { \pmb \rho }$ preserves perfect utility (after desanitization). We refer to such prompts as invariant prompts, where the LLM’s response should be invariant to the specific values (or small variations) of the sensitive tokens. This property holds in particular for prompts containing only type $\tau _ { \ I }$ tokens. Translation is exemplar: all sensitive tokens will be classified as type $\tau _ { \ I }$ and sanitized using FPE since the LLM’s translation should not depend on their specific values. As a result, sanitized tokens can be perfectly desanitized from the translated text. The quality score (the output of $Q$ ) can be evaluated using metrics such as BLEU score [83].

We now turn to the case of invariant prompts that include sensitive tokens of type $\tau _ { \ I \ I }$ . One such example is a factual information retrieval task for RAG. Consider the following prompt in the context of financial documents: “Please return all bank accounts with balance greater than $\$ 2000$ .” Here the two sensitive tokens $[ B a n k ~ A / C ]$ and [Bank Balance] are sanitized via FPE and mLDP, respectively. mLDP, by construction, noisily maps an input to a value that is close to it (as per Properties 1 and 2 in Sec. 4.1.2). As a consequence, the bank balance is perturbed only slightly, allowing correct numeric comparisons with high probability. This is precisely the rationale for our choice of mLDP: sanitized tokens preserve ordinal relationships and remain close to their original values, enabling useful computations while still providing strong privacy guarantees. The quality score here is the accuracy of the answers (count of the correct bank A/Cs returned). The above discussion is validated by our experimental results in Sec. 5. Formally, we have:

Theorem 4. For invariant prompts, Prϵϵmpt satisfies $( \alpha , \alpha )$ - utility where $\begin{array} { r l r } { \alpha } & { { } = } & { \mathbb { E } _ { f } \Big [ Q \big ( \pmb { \rho } , f ( \pmb { \rho } ) \big ) \Big ] \quad = } \end{array}$ $\mathbb { E } _ { f , P r \epsilon \epsilon m p t } \Big [ Q \Big ( \rho , D _ { P r \epsilon \epsilon m p t } \big ( K , f ( \hat { \rho } ) \big ) \Big ) \Big ] .$

Other Prompts. Given the complex and open-ended nature of prompts and responses, it is challenging to assign a utility score for any general prompt. Nevertheless, we provide some guidelines for when Prϵϵmpt is likely to perform well.

Note that Prϵϵmpt introduces only small perturbations in the sanitized prompt $\rho$ . Hence, intuitively, Prϵϵmpt should perform well where small changes in the original prompt result in only limited changes to the generated response. There can be two natural ways to capture these changes in the response. First, consider cases where the prompt satisfies Lipschitz continuity [77], as given by $d \mathsf { v } ( f ( \pmb { \rho } ) , f ( \hat { \pmb { \rho } } ) ) \leq K d \mathsf { v } ( \pmb { \rho } , \hat { \pmb { \rho } } )$ for some $K \in \mathbb { R } _ { > 0 }$ and distance metric $d \mathsf { v } : \mathsf { V } ^ { \ast } \times \mathsf { V } ^ { \ast } \mapsto \mathbb { R } _ { > 0 }$ . Distances defined over a document embedding space could be apt for $d _ { \mathsf { V } }$ . For example, when using an LLM as a financial advisor with a prompt “My monthly salary is $\$ 123,000$ . Suggest a monthly savings plan.”, the response should ideally remain consistent (and hence, very close in the embedding space) even if the salary value is slightly altered to $\$ 11,500$ (via $\mathcal { M } _ { \epsilon }$ ). A second way of bounding changes in the response is when the operations of the LLM on the sensitive tokens can be expressed as a symbolic computation. For example; “My height is $1 5 8 \mathrm { c m }$ and weight is 94lb. Compute my BMI.” The BMI is computed via a fixed formula (i.e., a symbolic computation). These type of prompts ensure that the responses on $\hat { \boldsymbol \rho }$ can deviate from the original response in only a well-structured and predictable manner. Additionally, if this symbolic mapping is known, Prϵϵmpt could leverage this information during desanitization to improve utility further.

Usability. A key advantage of Prϵϵmpt is its ease of use: after type annotation, Prϵϵmpt employs predefined sanitizers to protect sensitive tokens without any manual configuration of custom rules or execution of ad hoc sanitization strategies. In the current prototype, $\Psi$ is treated as an optional user input. Importantly, while $\Psi$ can be used to improve performance—for example, through better privacy budget allocation—omitting it does not affect the privacy guarantees of Prϵϵmpt. As discussed in Sec. 4.5, $\Psi$ can also be automatically generated from the input prompt to capture functional dependencies between sensitive tokens, further enhancing usability.

# 4.7 Comparison with Strawman Solutions

Strawman Solution I: Redaction. One intuitive solution is to redact all sensitive tokens from the prompt. While this approach ensures perfect privacy, it severely impacts utility dependent on those sensitive tokens and can sometimes lead to a complete loss of functionality. We present an example in Sec. .5.1

Strawman Solution II: Substitution. An intuitive solution is to replace sensitive tokens with others of the same type using a lookup table. However, this method is not stateless, as desanitization requires access to the lookup tables, leading to scalability and security issues (see Sec. 4.3). The table size grows linearly with the number of sensitive tokens, and a separate table is needed for each user to prevent information leakage. In contrast, Prϵϵmpt only requires a fixed-size key per user, regardless of prompt number or length.

Strawman Solution III: Suppression. Consider the following sanitization strategy for the tokens of the second category $\left( \tau _ { \perp \perp } \right)$ : a numerical token is sanitized by simply setting its $k$ lowest order digits to 0, the intuition being that the LLM’s response is most likely to depend on the higher-order digits, thereby preserving utility while only leaking information about the numerical value at a coarser granularity. However, it is difficult to formally quantify its privacy guarantees. Prior work shows that such ad-hoc approaches are often vulnerable to attacks [36, 31, 76]. In contrast, the mLDP-based approach used in Prϵϵmpt offers a principled way of balancing this privacy/utility trade-off.

Additional Baseline: LLMs assisted obfuscation and deobfuscation. One could also attempt to use a LLM to obfuscate and deobfuscate sensitive information based on rules in the system prompt, and maintaining a state to recover information, such as [94]. However, the probabilistic nature of the LLM and lack of specifications preclude any rigorous privacy analysis.

# 5 Experiments

We evaluate the following questions:

Q1. How does Prϵϵmpt impact utility of realistic tasks compared to unsanitized performance?   
Q2. How does Prϵϵmpt compare against prior LLM based sanitization approaches?   
Q3. What is the impact of different technical design choices on Prϵϵmpt’s utility?

# 5.1 Utility Loss from Prϵϵmpt Sanitization

We tackle Q1 by applying Prϵϵmpt to four tasks: translation, retrieval-augmented generation (RAG), multi-turn financial question answering (Q/A), and long-context reading comprehension Q/A. These tasks represent a broad spectrum of real-world LLM applications where input prompts are likely to contain sensitive information.

Table 1: Semantic Textual Similarity scores of different methods for the Long-Context Q/A task. Higher value implies more similarity with the reference answer. “Plain Responses” refer to the responses for unsanitized inputs, and “References” indicate the ground truth responses. We find that Prϵϵmpt has a particularly high utility with respect to GPT-4o, outperforming prior methods. Prϵϵmpt uses Gemma-2 9B Instruct as the NER model for Gemini-1.5, and UniNER for Llama-3 and GPT-4o.   

<table><tr><td>STS Score</td><td>Llama-3</td><td>Prεepsilon</td><td>GPT-4o</td><td>Papillon GPT-4o</td></tr><tr><td>Plain Responses</td><td>0.839</td><td>0.849</td><td>0.934</td><td>0.854</td></tr><tr><td>References (GT)</td><td>0.514</td><td>0.722</td><td>0.510</td><td>0.458</td></tr></table>

Models. We use GPT-4o [80], Gemini-1.5 [45], and OPUS-MT for translations, RAG, and question-answering tasks. For named entity recognition (NER), we use Uni-NER [107], Llama-3 8B Instruct [2], and Gemma-2 9B Instruct [46]. We also use Llama-3 as a Q/A model for the long-context task.

Translation. Translation is a common use case for language models. However, business or bureaucratic emails containing sensitive information face major privacy concerns pertaining to leakage of sensitive information [68]. For this task, we employ an LLM for named entity recognition (NER) of sensitive tokens belonging to the types of ([Name], [Age] and [Money]). We evaluate Prϵϵmpt’s performance on 50 English-French and English-German samples obtained from WMT-14 [14] dataset. These samples are single sentences containing one or two PII values. We seek exact translations in this context and use BLEU scores as the quality oracle $\mathcal { Q }$ to assess their similarity to reference translations. We use FPE to sanitize [Name] and [Money], and use $m L D P$ for $[ A g e ]$ .

Results. We report the BLEU scores for the translations of the original sentences and the ones obtained via Prϵϵmpt in Table 3. We observe that the BLEU scores are nearly identical in both cases, with only minor differences due to the performance variation of the translation model, nuances of language and NER. Details regarding the statistics of PII values, NER performance, details regarding encryption and ablations with larger privacy budgets can be found in App. .4.2. We present comparisons with Papillon [94], a contemporary privacy preserving framework in Section 5.2.

Retrieval-Augmented Generation (RAG). Retrieval-augmented generation is also commonly employed for a variety of LLM use cases [44], including extraction of information from potentially sensitive documents. Typically, documents are split, embedded, and indexed in a vector database. At query time, the most relevant shards are retrieved based on lexical and semantic similarity, then provided as context to the LLM for answer generation. Our experiments focus on this final step: generating answers given a query and its relevant context. We consider two types of question-answering scenarios: numerical comparisons, and retrieval of factual information. We assess these settings by using GPT-4 [80] to generate tuples of Context C, questions Questions Q, and answers Answers A; jointly sanitizing C and Q so that copies of the same sensitive attribute appearing in both C and Q are replaced with the same token, and comparing the desanitized LLM responses with A. Our numerical comparison questions involve comparing credit card balances and determining which is higher, while factual retrieval questions require returning specific aspects about a generated e-commerce order. The quality oracle $\mathcal { Q }$ is the accuracy of the answers.

Results. We observe that Prϵϵmpt achieves $1 0 0 \%$ accuracy for both the RAG tasks. Additional experimental details can be found in App. .4.3

Long-Context Q/A. LLMs can be tasked with not only retrieving specific information from long documents, but also integrating and reasoning about the information they contain. To simulate this, we use NarrativeQA [63], a longcontext, reading comprehension task. We answer questions about book or movie summaries, including characterrelated queries, using only the provided context. Character names are treated as sensitive attributes and sanitized using FPE. Summaries have 534 words on average with a standard deviation of 210.

To assess the impact of Prϵϵmpt on reasoning and reading comprehension, we use semantic textual similarity (STS) [86] between the answers based on the original summaries and the answers based on Prϵϵmpt summaries. This score also acts as the quality oracle Q. We do not use BLEU scores for this experiment, as the reference answers only have a few words and do not capture any paraphrased response. We discuss the performance of NER and present examples in App. .4.5. We present comparisons with Papillon [94], a contemporary privacy preserving framework in Sec. 5.2.

Results. We report the STS scores in Table 1. We find that Prϵϵmpt captures a significant amount of semantics of the plaintext response, with the GPT-4o response having an STS score of 0.934. For context, if we don’t desanitize the LLM response, the score drops to 0.523 with respect to the plain responses. If the LLM gives a completely irrelevant response (such as the answer to an unrelated question), the score drops to around 0.146. This demonstrates the robustness of the metric. Further details and ablations can be found in App .4.5.

Table 2: Performance evaluation on ConvFinQA benchmark with varying degrees of prompt sanitization (ϵ represents the privacy parameter for mLDP). Higher relative error indicates larger deviation from ground truth, while lower prediction consistency indicates a low relative discrepancy between sanitized and unsanitized responses. “Base” here indicates the baseline.   

<table><tr><td colspan="7">Impact of Preempt on ConvFinQA Performance</td></tr><tr><td rowspan="2">€</td><td colspan="3">Relative Error</td><td colspan="3">Prediction Consistency</td></tr><tr><td>25th</td><td>Median</td><td>75th</td><td>25th</td><td>Median</td><td>75th</td></tr><tr><td>0.1</td><td>0.0581</td><td>0.4000</td><td>4.4115</td><td>0.0698</td><td>0.3661</td><td>0.9994</td></tr><tr><td>0.5</td><td>0.0154</td><td>0.0776</td><td>1.0000</td><td>0.0167</td><td>0.1345</td><td>0.9898</td></tr><tr><td>1.0</td><td>0.0075</td><td>0.0408</td><td>0.9881</td><td>0.0084</td><td>0.0736</td><td>0.9899</td></tr><tr><td>2.0</td><td>0.0040</td><td>0.0244</td><td>0.8686</td><td>0.0044</td><td>0.0447</td><td>0.9899</td></tr><tr><td>Base</td><td>0.0000</td><td>0.0000</td><td>12.6749</td><td>-</td><td>-</td><td>-</td></tr></table>

Multi-Turn Financial Q/A. LLMs are also frequently used in multi-turn conversational settings, and may be tasked with performing numerical reasoning over sensitive information. Thus, we assess Prϵϵmpt on a financial multi-turn question answering benchmark ConvFinQA [28].The dataset consists of financial reports written by experts [29] followed by a sequence of conversational, numerical-reasoning questions guiding the model through solving a multi-step problem. Each prompt includes background text and a table with yearly financial data spanning over several years. All numerical information (except years) is extracted using regex and sanitized using mLDP. To handle repeated values within parentheses in the table, we use the helper string $\Psi$ in the regex updating of text to ensure that this structure is preserved in the sanitized text. ConvFinQA performance is typically reported in terms of exact match accuracy of responses. Since sanitization introduces noise in the numerical values, exact matching is no longer an appropriate evaluation criterion; instead, we measure utility after sanitization with the relative error of the prediction. Moreover, we observed that for this dataset, the answers returned by a model are occasionally correct up to the target answers sign or magnitude—often due to the questions being underspecified rather than model error. To account for the sensitivity of relative error to incorrect magnitudes of predictions, we check if the relative error of the magnitude and sign adjusted response is less than .1 of the correct answer. If the adjusted error is sufficiently small, we record it instead.

Results. We report the 25th, 50th, and 75th percentiles of the relative error in GPT-4o’s answers for sanitized and clean prompts. We further report the 25th, 50th, and 75th percentiles of “consistency”, measured as the relative difference between the model’s prediction on the sanitized query compared to the prediction on the clean query. We report the results in Table 2, observing a clear trend of performance improvement with a larger privacy budget, however, we note that at the 75th percentile, consistency does not change much. We also observe that the relative error of the sanitized prompts at the 75th percentile is lower than for unsanitized prompts, suggesting that addition of noise regularizes model behavior and prevents large outlier responses. We provide additional results with higher privacy budgets in App. .4.6.

# 5.2 Comparison of Prϵϵmpt with Prior Methods

We compare Prϵϵmpt with Papillon [94], a contemporary privacy-preserving framework. It uses a local LLM to create a proxy of the user query that omits all PII values, while attaining high utility with respect to a remote, task-performing model. We consider two tasks in our setting: Translation and Long-Context Q/A. We use GPT-4o for all steps of Papillon, with Llama-3.1 8B Instruct [2] as the local model.

Translation. We consider 100 samples for each sensitive attribute ([Name],[Age],[Money]) for both languages, for a total of 600 samples. Following Papillon, we create optimized prompts for each attribute-language pair.

Results. We report BLEU scores in Table 3. We find that Prϵϵmpt significantly outperforms Papillon, except for the [Age] and [Money] PII categories for the English-French translation task, where it is comparable. Furthermore, the average leakage of privacy due to NER failure is $7 1 \%$ of unique PII values compared to $9 \hat { 7 } \%$ for Prϵϵmpt. We detail their relative performance in App. .5.2.

Long-Context Q/A. We consider 50 samples for prompt optimization. Each sample contains a unique summary, a question based on it, and the corresponding answer.

Results. We report the STS scores in Table 1. We find that Prϵϵmpt performs somewhat better than Papillon. However, Papillon as implemented, is mostly unsuccessful in preventing leakage for long context tasks. We observed that $8 0 \%$ of all prompts passed to the remote model contain character identities. These prompts are just the questions and do not include the summary. As the summaries are based off Wikipedia entries, the remote model is able to identify those

Table 3: BLEU scores for the English German and English French translation tasks, with UniNER-7B-PII for NER. All scores are w.r.t the reference translations from WMT-14. Higher value implies more similarity with the reference translation. We find that Prϵϵmpt has nearly identical performance with the translations of unmodified sentences and also outperforms prior methods.   

<table><tr><td colspan="6">English → German, NER: UniNER-7B-PII</td></tr><tr><td rowspan="2">Attribute</td><td colspan="2">Gemini-1.5</td><td colspan="3">GPT-4o</td></tr><tr><td>Plain</td><td>Pre€empt</td><td>Plain</td><td>Pre€empt</td><td>Papillon</td></tr><tr><td>Name</td><td>0.334</td><td>0.341</td><td>0.287</td><td>0.278</td><td>0.175</td></tr><tr><td>Age</td><td>0.235</td><td>0.252</td><td>0.243</td><td>0.231</td><td>0.135</td></tr><tr><td>Money</td><td>0.245</td><td>0.274</td><td>0.217</td><td>0.200</td><td>0.153</td></tr><tr><td colspan="6">English → French, NER: UniNER-7B-PII</td></tr><tr><td>Name</td><td>0.423</td><td>0.408</td><td>0.432</td><td>0.419</td><td>0.290</td></tr><tr><td>Age</td><td>0.486</td><td>0.490</td><td>0.480</td><td>0.479</td><td>0.409</td></tr><tr><td>Money</td><td>0.329</td><td>0.333</td><td>0.294</td><td>0.279</td><td>0.299</td></tr></table>

Table 4: Named entity recognition (NER) F1 scores for English (E), German (G), and French (F). Our finetuned version of UniNER either matches or outperforms all other models on almost every sensitive attribute. “CCN” and “PN” stand for Credit Card Number and Phone Number respectively.   

<table><tr><td rowspan="3">Attribute</td><td colspan="9">Part A: Open-source Models</td><td colspan="8">Part B: Closed-source Models</td><td></td></tr><tr><td colspan="3">Uni-NER-7B-PII</td><td colspan="3">Gemma-2 9B Inst</td><td colspan="3">Llama-3.1 8B Inst</td><td colspan="3">GPT-4.1</td><td colspan="3">Gemini-2.5</td><td colspan="3">Claude 4 Sonnet</td></tr><tr><td>E</td><td>G</td><td>F</td><td>E</td><td>G</td><td>F</td><td>E</td><td>G</td><td>F</td><td>E</td><td>G</td><td>F</td><td>E</td><td>G</td><td>F</td><td>E</td><td>G</td><td>F</td></tr><tr><td>Name</td><td>1.00</td><td>1.00</td><td>1.00</td><td>.907</td><td>.893</td><td>.846</td><td>.836</td><td>.766</td><td>.715</td><td>.843</td><td>.883</td><td>.845</td><td>.742</td><td>.903</td><td>.840</td><td>.791</td><td>.867</td><td>.872</td></tr><tr><td>Age</td><td>1.00</td><td>1.00</td><td>1.00</td><td>1.00</td><td>.951</td><td>.990</td><td>.960</td><td>.884</td><td>.822</td><td>.970</td><td>1.00</td><td>.990</td><td>.990</td><td>.990</td><td>.990</td><td>.980</td><td>1.00</td><td>.990</td></tr><tr><td>Money</td><td>.940</td><td>.860</td><td>.880</td><td>.940</td><td>.827</td><td>.824</td><td>.820</td><td>.710</td><td>.820</td><td>.882</td><td>.941</td><td>.959</td><td>.990</td><td>1.00</td><td>1.00</td><td>.990</td><td>.980</td><td>1.00</td></tr><tr><td>SSN</td><td>.990</td><td>1.00</td><td>.990</td><td>.640</td><td>.760</td><td>.653</td><td>.843</td><td>.871</td><td>.827</td><td>.875</td><td>.959</td><td>.960</td><td>.990</td><td>1.00</td><td>1.00</td><td>.969</td><td>.969</td><td>.929</td></tr><tr><td>CCN</td><td>.980</td><td>.960</td><td>1.00</td><td>.952</td><td>.962</td><td>.873</td><td>.916</td><td>.926</td><td>.855</td><td>.971</td><td>.971</td><td>.980</td><td>.980</td><td>.990</td><td>.970</td><td>.980</td><td>.980</td><td>.980</td></tr><tr><td>Zipcode</td><td>1.00</td><td>.990</td><td>.980</td><td>.980</td><td>.990</td><td>.980</td><td>.952</td><td>.925</td><td>.936</td><td>.980</td><td>.962</td><td>.981</td><td>.990</td><td>.980</td><td>.990</td><td>.990</td><td>.942</td><td>.990</td></tr><tr><td>Date</td><td>1.00</td><td>1.00</td><td>1.00</td><td>.778</td><td>.708</td><td>.649</td><td>.960</td><td>.846</td><td>.895</td><td>1.00</td><td>.980</td><td>.970</td><td>.860</td><td>.733</td><td>.784</td><td>1.00</td><td>.971</td><td>.980</td></tr><tr><td>Password</td><td>.980</td><td>1.00</td><td>1.00</td><td>.885</td><td>.887</td><td>.833</td><td>.238</td><td>.087</td><td>.163</td><td>1.00</td><td>.970</td><td>.950</td><td>.980</td><td>.810</td><td>.970</td><td>.990</td><td>.970</td><td>.922</td></tr><tr><td>Sex</td><td>1.00</td><td>1.00</td><td>1.00</td><td>.971</td><td>.943</td><td>.980</td><td>.926</td><td>.673</td><td>.830</td><td>.962</td><td>.945</td><td>.971</td><td>.971</td><td>.925</td><td>.990</td><td>.971</td><td>.954</td><td>.980</td></tr><tr><td>PN</td><td>.980</td><td>1.00</td><td>1.00</td><td>.952</td><td>.971</td><td>.962</td><td>.926</td><td>.971</td><td>.971</td><td>.980</td><td>.970</td><td>.990</td><td>.990</td><td>1.00</td><td>.990</td><td>.980</td><td>.980</td><td>.990</td></tr></table>

characters and correctly respond to the query. We discuss NER performance and examples of successes and failures in App. .5.3.

# 5.3 Impact of Design Choices on Prϵϵmpt Utility

To address Q3, we examine design choices for two components: NER and encryption format.

Named-Entity Recognizer (NER). Uni-NER [107] is an LLM trained for generic named entity recognition. We finetune it on 10 high-risk categories from the AI4Privacy dataset [1]. We evaluate the NER as a type annotator on a held out subset of the dataset, consisting of text in English, German and French, with 50 samples per category, per language. We tabulate results for the following categories: “Money”, “Name”, “Age”, “SSN”, “Credit Card Number”, “Zipcode”, “Date”, “Password”, “Sex”, “Phone Number”. We make comparisons with off-the-shelf proprietary and open-source models, including: GPT-4.1 [81], Claude 4 Sonnet [7], Gemini 2.5 [62], Llama-3.1 8B Instruct [2] and Gemma-2 9B Instruct [46] (details in App. .6.1). As our experiments only deal with Name, Age and Money, we use another Uni-NER model, specifically finetuned on these attributes.

Results. As seen in Table 4 (App. .6.1), fine-tuning Uni-NER on these high-risk categories yields $100 \%$ F-1 scores across most attributes, often exceeding the performance of state-of-the-art proprietary models.

Encryption Format. Prϵϵmpt assumes that the LLM’s performance depends on preserving the format of type $\tau _ { \ I }$ tokens. We validate this assumption by evaluating the LLM on two other sanitization algorithms: (1) that does not preserve the format at all, and (2) that preserves an incorrect format. For the first case, we sanitize the type $\tau _ { \ I }$ tokens with AES, which replaces the sensitive tokens with 16 bytes of random strings. In the second case, we randomly substitute the tokens without maintaining the correct format (e.g. replacing a 5-digit ZIP code with a randomly chosen 8-digit value). We assess this in the context of a RAG task by generating 31 tuples of contexts (C), questions (Q), and answers (A) corresponding to a factual retrieval task. For each tuple, we evaluate the percentage of correct, desanitized answers using GPT-4.

Table 5: A comparison of prompt sanitization frameworks as per the design goals in Sec. 4.3. We find that Prϵϵmpt is the only framework that has all the desirable qualities of a secure and high utility prompt sanitizer.   

<table><tr><td>Method</td><td>Stateless</td><td>Formal Privacy Guarantee</td><td>High Utility</td><td>Resource-Efficient</td></tr><tr><td>Preempt (Ours)</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>Papillon [94]</td><td>✗</td><td>✗</td><td>✓</td><td>✓</td></tr><tr><td>Substitution-based [91, 61, 27]</td><td>✗</td><td>✗</td><td>✓</td><td>✓</td></tr><tr><td>Cryptography-based [54, 49, 26]</td><td>✓</td><td>✓</td><td>✓</td><td>✗</td></tr><tr><td>DP-based noisiging of text [34, 97, 52, 99]</td><td>✓</td><td>✓</td><td>✗</td><td>✗</td></tr><tr><td>DP-based noisiging of text embeddings [43]</td><td>✓</td><td>✓</td><td>✗</td><td>✓</td></tr><tr><td>DP-based noisiging of tokens [20, 9, 10, 25]</td><td>✓</td><td>✓</td><td>✗</td><td>✓</td></tr><tr><td>DP-based text paraphrasing [71, 101, 65, 55]</td><td>✓</td><td>✓</td><td>✗</td><td>✓</td></tr></table>

Results. We observe that our model achieves $100 \%$ accuracy in factual information retrieval when employing FPE. However, performance drops to $7 0 . 9 7 \%$ with AES encryption and $7 7 . 4 2 \%$ with random substitution using incorrect formats. This confirms that format preservation is crucial for the LLM’s performance. We provide additional results for the Translation and Multi-Turn Financial Q/A tasks with different privacy budgets in App. .4.2 and App. .4.6 respectively.

# 6 Related Work

A line of work proposes to sanitize the prompts via substitution using a local LLM[91, 61, 27]. However, such solutions cannot be stateless if they intend to provide utility by desanitizing LLM responses. Cryptographic methods have also been explored for protecting user privacy at inference [54, 49, 26]. However, these approaches impose high computational and communication overheads. One line of approach for protecting privacy at inference involves employing DP for in-context learning by generating a synthetic dataset [34, 97, 52, 99]. However, these approaches are only applicable when a large collection of data is available, and are different from sanitizing an individuals sensitive information when they are submitting a simple query to an LLM. More similar to our setting are local DP based approaches. However, a key difference from our work is the way in which noise is added. A line of prior work employs metric DP by adding noise to text embeddings, and then decoding the private embeddings back into text [43]: this violates the definition of a prompt sanitizer as this might not preserve the types of the tokens (Sec. 3). Another approach noisily sample a token from a pre-defined list of “similar” tokens [20, 9, 10, 25] which require carefully selecting the list of similar tokens. Another line of work generates a noisy paraphrase of the prompts [71, 101, 65, 55]. However, these methods suffer from the curse of dimensionality as the amount of noise grows proportionally with the length of the generated text leading to poor utility. Table 5 provides a summary comparing Prϵϵmpt with prior work.

# 7 Conclusion

LLMs introduce new challenges for protecting sensitive information at inference time. We address this by introducing a cryptographically inspired primitive—the prompt sanitizer—which transforms prompts to protect sensitive tokens. We then present Prϵϵmpt, a system that implements this primitive with provable privacy guarantees. Experiments show that Prϵϵmpt maintains high utility across both structured and open-ended prompts.

# Availability

An implementation of Prϵϵmpt and experimental results can be found at [48].

# Acknowledgements

David Glukhov and Nicolas Papernot would like to acknowledge their sponsors, who support their research with financial and in-kind contributions: Amazon, Apple, CIFAR through the Canada CIFAR AI Chair, Microsoft, Meta, NSERC through the Discovery Grant and two Alliance Grants with ServiceNow and DRDC and with CSE, the Ontario Early Researcher Award, and the Schmidt Sciences foundation through the AI2050 Early Career Fellow program. Resources used in preparing this research were provided, in part, by the Province of Ontario, the Government of Canada through CIFAR, and companies sponsoring the Vector Institute.

Divyam Anshumaan and Somesh Jha are partially supported by DARPA under agreement number 885000, NSF CCF-FMiTF-1836978 and ONR N00014-21-1-2492.

# 8 Ethical Considerations

We provide a framework for enabling users to sanitize sensitive tokens before submitting prompts to proprietary LLMs. To evaluate our framework, we generated synthetic data for sensitive tokens, avoiding issues of using or releasing sensitive data of any individuals. While theoretically sound, there still exist practical limitations of our sanitization procedure, for example imperfect detection of types by NER methods, that could result in sensitive attributes being leaked. Furthermore, LLMs may still behave more erratically on tail events and it is possible that sanitization could result in inputs that significantly alter model behavior. If these limitations are ignored, usage of our framework could lead to a false sense of safety by the user. As such, we do not make claims that our method is always effective and we provide empirical evidence demonstrating failure modes. Furthermore, our theoretical analysis provides a useful step forward for the problem of prompt sanitization, and we highlight several often overlooked issues of prior work on text sanitization work.

We also emphasize that our toy Financial settings is not intended to illustrate recommended use cases for our approach, particularly as questions regarding financial and medical decision making should be addressed to certified professionals as opposed to LLMs. Nevertheless, many users may still decide to interact with LLMs in this manner and risk revealing sensitive information in the process. We studied these settings specifically for the purpose of understanding the how sanitiztion affects model decision making in such ill-specified settings where there is no “correct answer” but a model must still make a decision. As such, our results reflect reasoning and robustness of LLMs to sanitization methods.

# References

[1] ai4Privacy. pii-masking-200k (Revision 1d4c0a1). 2023. DOI: 10.57967/hf/1532. URL: https:// huggingface.co/datasets/ai4privacy/pii-masking-200k.   
[2] Abhimanyu Dubey et al. The Llama 3 Herd of Models. 2024. arXiv: 2407.21783 [cs.AI]. URL: https: //arxiv.org/abs/2407.21783.   
[3] M. Alvim et al. “Invited Paper: Local Differential Privacy on Metric Spaces: Optimizing the Trade-Off with Utility”. In: 2018 IEEE 31st Computer Security Foundations Symposium (CSF). 2018, pp. 262–267.   
[4] Amazon Implements Restrictions on the Use of Generative AI Tools by Employees. https : / / www . neatprompts . com / p / amazon - implements - restrictions - on - the - use - of - generative-ai-tools-by-employees. 2024.   
[5] Miguel E. Andres et al. “Geo-indistinguishability: differential privacy for location-based systems”. In: ´ Proceedings of the 2013 ACM SIGSAC conference on Computer & communications security - CCS ’13. CCS ’13. ACM Press, 2013, pp. 901–914. DOI: 10.1145/2508859.2516735. URL: http://dx.doi.org/ 10.1145/2508859.2516735.   
[6] Rohan Anil et al. Large-Scale Differentially Private BERT. 2021. arXiv: 2108.01624 [cs.LG].   
[7] Anthropic. Claude 4 Sonnet. 2025. URL: https://www.anthropic.com/claude/sonnet.   
[8] Apple restricts employees from using ChatGPT over fear of data leaks. https://www.theverge.com/ 2023/5/19/23729619/apple-bans-chatgpt-openai-fears-data-leak. 2023.   
[9] Stefan Arnold et al. “Driving Context into Text-to-Text Privatization”. In: arXiv preprint arXiv:2306.01457 (2023).   
[10] Stefan Arnold et al. Guiding Text-to-Text Privatization by Syntax. 2023. arXiv: 2306.01471 [cs.CL].   
[11] Clark Barrett et al. Identifying and Mitigating the Security Risks of Generative AI. 2023. arXiv: 2308.14840 [cs.AI].   
[12] Mihir Bellare et al. Format-Preserving Encryption. Cryptology ePrint Archive, Paper 2009/251. https : //eprint.iacr.org/2009/251. 2009. URL: https://eprint.iacr.org/2009/251.   
[13] Mihir Bellare et al. “Format-Preserving Encryption”. In: Selected Areas in Cryptography: 16th Annual International Workshop, SAC 2009, Calgary, Alberta, Canada, August 13-14, 2009, Revised Selected Papers. Berlin, Heidelberg: Springer-Verlag, 2009, pp. 295–312. ISBN: 9783642054433. URL: https : / / doi . org/10.1007/978-3-642-05445-7_19.   
[14] Ondˇrej Bojar et al. “Findings of the 2014 Workshop on Statistical Machine Translation”. In: Proceedings of the Ninth Workshop on Statistical Machine Translation. Ed. by Ondˇrej Bojar et al. Baltimore, Maryland, USA: Association for Computational Linguistics, June 2014, pp. 12–58. DOI: 10.3115/v1/W14-3302. URL: https://aclanthology.org/W14-3302.

[15] Hannah Brown et al. What Does it Mean for a Language Model to Preserve Privacy? 2022. arXiv: 2202. 05520 [stat.ML].   
[16] Hannah Brown et al. “What Does it Mean for a Language Model to Preserve Privacy?” In: Proceedings of the 2022 ACM Conference on Fairness, Accountability, and Transparency. FAccT ’22. Seoul, Republic of Korea: Association for Computing Machinery, 2022, pp. 2280–2292. ISBN: 9781450393522. DOI: 10.1145/ 3531146.3534642. URL: https://doi.org/10.1145/3531146.3534642.   
[17] Tom Brown et al. “Language models are few-shot learners”. In: Advances in neural information processing systems 33 (2020), pp. 1877–1901.   
[18] California Consumer Privacy Act (CCPA). https://oag.ca.gov/privacy/ccpa. 2018.   
[19] Nicholas Carlini et al. “Extracting training data from large language models”. In: 30th USENIX Security Symposium (USENIX Security 21). 2021, pp. 2633–2650.   
[20] Ricardo Silva Carvalho et al. “TEM: High Utility Metric Differential Privacy on Text”. In: ArXiv abs/2107.07928 (2021). URL: https://api.semanticscholar.org/CorpusID:236034456.   
[21] Ricardo Silva Carvalho et al. “TEM: High Utility Metric Differential Privacy on Text”. In: Proceedings of the 2023 SIAM International Conference on Data Mining (SDM), pp. 883–890. DOI: 10 . 1137 / 1 . 9781611977653 . ch99. eprint: https : / / epubs . siam . org / doi / pdf / 10 . 1137 / 1 . 9781611977653 . ch99. URL: https : / / epubs . siam . org / doi / abs / 10 . 1137 / 1 . 9781611977653.ch99.   
[22] ChatGPT Is Banned in Italy Over Privacy Concerns. https://www.nytimes.com/2023/03/31/ technology/chatgpt-italy-ban.html. 2023.   
[23] Konstantinos Chatzikokolakis et al. “Broadening the scope of differential privacy using metrics”. In: PETS. 2013.   
[24] Sai Chen et al. “A Customized Text Sanitization Mechanism with Differential Privacy”. In: Findings of the Association for Computational Linguistics: ACL 2023. Ed. by Anna Rogers et al. Toronto, Canada: Association for Computational Linguistics, July 2023, pp. 5747–5758. DOI: 10 . 18653 / v1 / 2023 . findings - acl.355. URL: https://aclanthology.org/2023.findings-acl.355/.   
[25] Sai Chen et al. “A customized text sanitization mechanism with differential privacy”. In: Findings of the Association for Computational Linguistics: ACL 2023. 2023, pp. 5747–5758.   
[26] Tianyu Chen et al. “The-x: Privacy-preserving transformer inference with homomorphic encryption”. In: arXiv preprint arXiv:2206.00216 (2022).   
[27] Yu Chen et al. “Hide and seek (has): A lightweight framework for prompt privacy protection”. In: arXiv preprint arXiv:2309.03057 (2023).   
[28] Zhiyu Chen et al. ConvFinQA: Exploring the Chain of Numerical Reasoning in Conversational Finance Question Answering. 2022. arXiv: 2210 . 03849 [cs.CL]. URL: https : / / arxiv . org / abs / 2210 . 03849.   
[29] Zhiyu Chen et al. FinQA: A Dataset of Numerical Reasoning over Financial Data. 2022. arXiv: 2109.00122 [cs.CL]. URL: https://arxiv.org/abs/2109.00122.   
[30] Amrita Roy Chowdhury et al. Strengthening Order Preserving Encryption with Differential Privacy. 2022. arXiv: 2009.05679 [cs.CR]. URL: https://arxiv.org/abs/2009.05679.   
[31] Aloni Cohen. “Attacks on Deidentification’s Defenses”. In: 31st USENIX Security Symposium (USENIX Security 22). Boston, MA: USENIX Association, Aug. 2022, pp. 1469–1486. ISBN: 978-1-939133-31-1. URL: https://www.usenix.org/conference/usenixsecurity22/presentation/cohen.   
[32] Jiaxi Cui et al. “Chatlaw: Open-source legal large language model with integrated external knowledge bases”. In: arXiv preprint arXiv:2306.16092 (2023).   
[33] Doctors banned from using ChatGPT to write medical notes. https://www.ausdoc.com.au/news/ doctors-banned-from-using-chatgpt-to-write-medical-notes/. 2023.   
[34] Haonan Duan et al. “Flocks of stochastic parrots: differentially private prompt learning for large language models”. In: Proceedings of the 37th International Conference on Neural Information Processing Systems. NIPS ’23. New Orleans, LA, USA: Curran Associates Inc., 2024.   
[35] Cynthia Dwork et al. 2014. DOI: 10.1561/0400000042.   
[36] Cynthia Dwork et al. “Exposed! A Survey of Attacks on Private Data”. In: Annual Review of Statistics and Its Application 4 (2017), pp. 61–84. URL: https : / / api . semanticscholar . org / CorpusID : 26766335.   
[37] Cynthia Dwork et al. “The Algorithmic Foundations of Differential Privacy”. In: Found. Trends Theor. Comput. Sci. 9.3&#8211;4 (Aug. 2014), pp. 211–407. ISSN: 1551-305X.

[38] Cynthia Dwork et al. “The Algorithmic Foundations of Differential Privacy”. In: Found. Trends Theor. Comput. Sci. 9.3–4 (Aug. 2014), pp. 211–407. ISSN: 1551-305X. DOI: 10 . 1561 / 0400000042. URL: https : //doi.org/10.1561/0400000042.   
[39] Morris J. Dworkin. “800-38 G Recommendation for Block Cipher Modes of Operation : Methods for Format-Preserving Encryption”. In: 2013. URL: https : / / api . semanticscholar . org / CorpusID : 34369021.   
[40] Stefan Dziembowski et al. “Leakage-resilient cryptography”. In: 2008 49th Annual IEEE Symposium on Foundations of Computer Science. IEEE. 2008, pp. 293–302.   
[41] Natasha Fernandes et al. Generalised Differential Privacy for Text Document Processing. 2019. arXiv: 1811. 10256 [cs.CR]. URL: https://arxiv.org/abs/1811.10256.   
[42] Oluwaseyi Feyisetan et al. “Leveraging Hierarchical Representations for Preserving Privacy and Utility in Text”. In: 2019 IEEE International Conference on Data Mining (ICDM). 2019, pp. 210–219. DOI: 10.1109/ ICDM.2019.00031.   
[43] Oluwaseyi Feyisetan et al. “Privacy-and utility-preserving textual analysis via calibrated multivariate perturbations”. In: Proceedings of the 13th international conference on web search and data mining. 2020, pp. 178– 186.   
[44] Yunfan Gao et al. “Retrieval-augmented generation for large language models: A survey”. In: arXiv preprint arXiv:2312.10997 (2023).   
[45] Petko Georgiev et al. Gemini Team. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. 2024. arXiv: 2403.05530 [cs.CL]. URL: https://arxiv.org/abs/2403. 05530.   
[46] Morgane Riviere et al. Gemma Team. Gemma 2: Improving Open Language Models at a Practical Size. 2024. arXiv: 2408.00118 [cs.CL]. URL: https://arxiv.org/abs/2408.00118.   
[47] General Data Protection Regulation GDPR. https://gdpr-info.eu/. 2016.   
[48] GitHub Repository. https://github.com/danshumaan/preempt. 2025.   
[49] Meng Hao et al. “Iron: Private inference on transformers”. In: Advances in neural information processing systems 35 (2022), pp. 15718–15731.   
[50] Peter Henderson et al. “Ethical Challenges in Data-Driven Dialogue Systems”. In: Proceedings of the 2018 AAAI/ACM Conference on AI, Ethics, and Society. AIES ’18. New Orleans, LA, USA: Association for Computing Machinery, 2018, pp. 123–129. ISBN: 9781450360128. DOI: 10.1145/3278721.3278777. URL: https://doi.org/10.1145/3278721.3278777.   
[51] Dan Hendrycks et al. “Measuring Massive Multitask Language Understanding”. In: International Conference on Learning Representations. 2021. URL: https://openreview.net/forum?id=d7KBjmI3GmQ.   
[52] Junyuan Hong et al. “Dp-opt: Make large language model your privacy-preserving prompt engineer”. In: arXiv preprint arXiv:2312.03724 (2023).   
[53] Shlomo Hoory et al. “Learning and Evaluating a Differentially Private Pre-trained Language Model”. In: PRIVATENLP. 2021. URL: https://api.semanticscholar.org/CorpusID:235097653.   
[54] Xiaoyang Hou et al. CipherGPT: Secure Two-Party GPT Inference. Cryptology ePrint Archive, Paper 2023/1147. 2023. URL: https://eprint.iacr.org/2023/1147.   
[55] Timour Igamberdiev et al. DP-BART for Privatized Text Rewriting under Local Differential Privacy. 2023. arXiv: 2302.07636 [cs.CR].   
[56] Jacob Imola et al. Metric Differential Privacy at the User-Level. 2024. arXiv: 2405.02665 [cs.CR]. URL: https://arxiv.org/abs/2405.02665.   
[57] Jacob Imola et al. “Metric Differential Privacy at the User-Level via the Earth-Mover’s Distance”. In: Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security. CCS ’24. ACM, Dec. 2024, pp. 348–362. DOI: 10.1145/3658644.3690363. URL: http://dx.doi.org/10. 1145/3658644.3690363.   
[58] Katharina Jeblick et al. “ChatGPT makes medicine easy to swallow: an exploratory case study on simplified radiology reports”. In: European Radiology (2023), pp. 1–9.   
[59] JPMorgan Chase Restricts Staffers’ Use Of ChatGPT. https : / / www . forbes . com / sites / siladityaray / 2023 / 02 / 22 / jpmorgan - chase - restricts - staffers - use - of - chatgpt/. 2023.   
[60] Firuz Kamalov et al. New Era of Artificial Intelligence in Education: Towards a Sustainable Multifaceted Revolution. 2023. arXiv: 2305.18303 [cs.CY].   
[61] Zhigang Kan et al. “Protecting user privacy in remote conversational systems: A privacy-preserving framework based on text sanitization”. In: arXiv preprint arXiv:2306.08223 (2023).

[62] Koray Kavukcuoglu. Gemini 2.5: Our most intelligent AI model. 2025. URL: https://blog.google/ technology / google - deepmind / gemini - model - thinking - updates - march - 2025 / #gemini-2-5-thinking.   
[63] Toma´s Ko ˇ cisk ˇ y et al. “The NarrativeQA Reading Comprehension Challenge”. In: ´ Transactions of the Association for Computational Linguistics 6 (2018). Ed. by Lillian Lee et al., pp. 317–328. DOI: 10.1162/tacl_ a_00023. URL: https://aclanthology.org/Q18-1023/.   
[64] Katherine Lee et al. “Deduplicating training data makes language models better”. In: arXiv preprint arXiv:2107.06499 (2021).   
[65] Mike Lewis et al. “BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension”. In: Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics. 2020, pp. 7871–7880.   
[66] Xuechen Li et al. Large Language Models Can Be Strong Differentially Private Learners. 2022. arXiv: 2110. 05679 [cs.LG].   
[67] Guo Lin et al. EmojiCrypt: Prompt Encryption for Secure Communication with Large Language Models. 2024. arXiv: 2402.05868 [cs.CL]. URL: https://arxiv.org/abs/2402.05868.   
[68] Chenyang Lyu et al. A Paradigm Shift: The Future of Machine Translation Lies with Large Language Models. 2024. arXiv: 2305.01181 [cs.CL]. URL: https://arxiv.org/abs/2305.01181.   
[69] M. Maffei et al. “On the Security of Frequency-Hiding Order-Preserving Encryption”. In: Cryptology and Network Security. Ed. by Srdjan Capkun et al. Cham: Springer International Publishing, 2018, pp. 51–70. ISBN: 978-3-030-02641-7.   
[70] Peihua Mai et al. “Split-and-Denoise: Protect large language model inference with local differential privacy”. In: arXiv preprint arXiv:2310.09130 (2023).   
[71] Justus Mattern et al. “The Limits of Word Level Differential Privacy”. In: Findings of the Association for Computational Linguistics: NAACL 2022. 2022, pp. 867–881.   
[72] H. Brendan McMahan et al. Learning Differentially Private Recurrent Language Models. 2018. arXiv: 1710. 06963 [cs.LG].   
[73] Niloofar Mireshghallah et al. Can LLMs Keep a Secret? Testing Privacy Implications of Language Models via Contextual Integrity Theory. 2023. arXiv: 2310.17884 [cs.AI].   
[74] Philip Moons et al. “ChatGPT: can artificial intelligence language models be of value for cardiovascular nurses and allied health professionals”. In: European Journal of Cardiovascular Nursing 22.7 (Feb. 2023), e55–e59. ISSN: 1474-5151. DOI: 10 . 1093 / eurjcn / zvad022. eprint: https : / / academic . oup . com / eurjcn/article-pdf/22/7/e55/52017892/zvad022.pdf. URL: https://doi.org/10. 1093/eurjcn/zvad022.   
[75] More federal agencies join in temporarily blocking or banning ChatGPT. https://fedscoop.com/ more-federal-agencies-join-in-temporarily-blocking-or-banning-chatgpt/. 2024.   
[76] Arvind Narayanan et al. “Myths and fallacies of ”Personally Identifiable Information””. In: Commun. ACM 53.6 (June 2010), pp. 24–26. ISSN: 0001-0782. DOI: 10 . 1145 / 1743546 . 1743558. URL: https : //doi.org/10.1145/1743546.1743558.   
[77] Jorge Nocedal et al. Numerical Optimization. 2e. New York, NY, USA: Springer, 2006.   
[78] Goldreich Oded. Foundations of Cryptography: Volume 2, Basic Applications. 1st. New York, NY, USA: Cambridge University Press, 2009. ISBN: 052111991X, 9780521119917.   
[79] Goldreich Oded. Foundations of Cryptography: Volume 2, Basic Applications. 1st. USA: Cambridge University Press, 2009. ISBN: 052111991X.   
[80] OpenAI. GPT-4 Technical Report. 2023. arXiv: 2303.08774 [cs.CL].   
[81] OpenAI. Introducing GPT-4.1 in the API. 2025. URL: https://openai.com/index/gpt-4-1/.   
[82] Q. Pang et al. “BOLT: Privacy-Preserving, Accurate and Efficient Inference for Transformers”. In: 2024 IEEE Symposium on Security and Privacy (SP). Los Alamitos, CA, USA: IEEE Computer Society, May 2024, pp. 133–133. DOI: 10 . 1109 / SP54263 . 2024 . 00130. URL: https : / / doi . ieeecomputersociety.org/10.1109/SP54263.2024.00130.   
[83] Kishore Papineni et al. “BLEU: a method for automatic evaluation of machine translation”. In: Proceedings of the 40th Annual Meeting on Association for Computational Linguistics. ACL ’02. Philadelphia, Pennsylvania: Association for Computational Linguistics, 2002, pp. 311–318. DOI: 10.3115/1073083.1073135. URL: https://doi.org/10.3115/1073083.1073135.

[84] Kishore Papineni et al. “Bleu: a Method for Automatic Evaluation of Machine Translation”. In: Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics. Ed. by Pierre Isabelle et al. Philadelphia, Pennsylvania, USA: Association for Computational Linguistics, July 2002, pp. 311–318. DOI: 10.3115/1073083.1073135. URL: https://aclanthology.org/P02-1040.   
[85] Swaroop Ramaswamy et al. Training Production Language Models without Memorizing User Data. 2020. arXiv: 2009.10031 [cs.LG].   
[86] Nils Reimers et al. “Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks”. In: Conference on Empirical Methods in Natural Language Processing. 2019. URL: https://api.semanticscholar. org/CorpusID:201646309.   
[87] Philippe Remy. Name Dataset. https://github.com/philipperemy/name-dataset. 2021.   
[88] Amrita Roy Chowdhury et al. “Strengthening Order Preserving Encryption with Differential Privacy”. In: Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security. CCS ’22. Los Angeles, CA, USA: Association for Computing Machinery, 2022, pp. 2519–2533. ISBN: 9781450394505. DOI: 10.1145/3548606.3560610. URL: https://doi.org/10.1145/3548606.3560610.   
[89] Samsung Bans ChatGPT Among Employees After Sensitive Code Leak. https://www.forbes.com/ sites/siladityaray/2023/05/02/samsung- bans- chatgpt- and- other- chatbotsfor-employees-after-sensitive-code-leak/. 2023.   
[90] Samsung Bans Staff’s AI Use After Spotting ChatGPT Data Leak. https://www.bloomberg.com/ news/articles/2023-05-02/samsung-bans-chatgpt-and-other-generative-aiuse-by-staff-after-leak?embedded-checkout $=$ true. 2023.   
[91] Zhili Shen et al. The Fire Thief Is Also the Keeper: Balancing Usability and Privacy in Prompts. 2024. arXiv: 2406.14318 [cs.CR]. URL: https://arxiv.org/abs/2406.14318.   
[92] Weiyan Shi et al. Selective Differential Privacy for Language Modeling. 2022. arXiv: 2108 . 12944 [cs.CL].   
[93] Karan Singhal et al. “Towards expert-level medical question answering with large language models”. In: arXiv preprint arXiv:2305.09617 (2023).   
[94] Li Siyan et al. “PAPILLON: PrivAcy Preservation from Internet-based and Local Language MOdel ENsembles”. In: arXiv preprint arXiv:2410.17127 (2024).   
[95] Social Security Administration issues temporary block on generative AI. https : / / fedscoop . com / social-security-administration-temporary-block-generative-ai/. 2023.   
[96] Space Force Pumps the Brakes on ChatGPT-Like Technology With Temporary Ban. https : / / www . airandspaceforces.com/space-force-chatgpt-technology-temporary-ban/. 2023.   
[97] Xinyu Tang et al. “Privacy-preserving in-context learning with differentially private few-shot generation”. In: arXiv preprint arXiv:2309.11765 (2023).   
[98] Om Dipakbhai Thakkar et al. “Understanding Unintended Memorization in Language Models Under Federated Learning”. In: Proceedings of the Third Workshop on Privacy in Natural Language Processing. Ed. by Oluwaseyi Feyisetan et al. Online: Association for Computational Linguistics, June 2021, pp. 1–10. DOI: 10 . 18653 / v1 / 2021 . privatenlp - 1 . 1. URL: https : / / aclanthology . org / 2021 . privatenlp-1.1.   
[99] Zhiliang Tian et al. “Seqpate: Differentially private text generation via knowledge distillation”. In: Advances in Neural Information Processing Systems 35 (2022), pp. 11117–11130.   
[100] Jorg Tiedemann et al. “OPUS-MT — Building open translation services for the World”. In: ¨ Proceedings of the 22nd Annual Conferenec of the European Association for Machine Translation (EAMT). Lisbon, Portugal, 2020.   
[101] Saiteja Utpala et al. “Locally differentially private document generation using zero shot prompting”. In: arXiv preprint arXiv:2310.16111 (2023).   
[102] Workers’ ChatGPT Use Restricted At More Banks—Including Goldman, Citigroup. https : / / www . forbes.com/sites/brianbushard/2023/02/24/workers-chatgpt-use-restrictedat-more-banks-including-goldman-citigroup/. 2023.   
[103] Da Yu et al. Differentially Private Fine-tuning of Language Models. 2022. arXiv: 2110.06500 [cs.LG].   
[104] Rowan Zellers et al. “HellaSwag: Can a Machine Really Finish Your Sentence?” In: Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics. Ed. by Anna Korhonen et al. Florence, Italy: Association for Computational Linguistics, July 2019, pp. 4791–4800. DOI: 10.18653/v1/P19-1472. URL: https://aclanthology.org/P19-1472/.   
[105] Hanlin Zhang et al. “Watermarks in the Sand: Impossibility of Strong Watermarking for Generative Models”. In: Forty-first International Conference on Machine Learning. 2024.

[106] Mengke Zhang et al. LatticeGen: A Cooperative Framework which Hides Generated Text in a Lattice for Privacy-Aware Generation on Cloud. 2024. arXiv: 2309.17157 [cs.CL]. URL: https://arxiv. org/abs/2309.17157.   
[107] Wenxuan Zhou et al. “UniversalNER: Targeted Distillation from Large Language Models for Open Named Entity Recognition”. In: (2023). arXiv: 2308.03279 [cs.CL].

# .1 Background on FPE

# Mechanism for ϵ-mLDP.

Algorithm 3 Mechanism Mϵ   
Input: $x$ - Plainext; $\epsilon$ - Privacy parameter; $[k]$ - Output domain  
Output: $o'$ - Noisy encoding;  
1: for $x\in \mathcal{X}$ 2: for $i\in [k]$ 3: $p_{x,i} = \frac{e^{-|x - i|\cdot\epsilon / 2}}{\sum_{j = 1}^{k}e^{-|x - j|\cdot\epsilon / 2}}$ (6)  
4: end for  
5: $p_x = \{p_{x,1},\dots ,p_{x,k}\}$ 6: end for  
7: $o\sim p_x$ 8: return o

Security Definition of FPEs. Pseudo-Random Permutation (PRP) security requires that an adversary cannot distinguish encryptions with a randomly chosen key from random permutations over the format domain; single-point indistinguishability (SPI) requires that the adversary cannot distinguish the encryption of any message of its choice from a random ciphertext; message privacy (MP) requires that ciphertexts reveal no information on the encrypted message, except its format; and similar to MP, but weaker than it, message recovery (MR) only requires that the ciphertext does not completely reveal the encrypted message. Bellare et al. [12] show that

$$
\mathrm {P R P} \Longleftrightarrow \mathrm {S P I} \Rightarrow \mathrm {M P} \Rightarrow \mathrm {M R} \tag {7}
$$

This implies that PRP is the strongest security notion and MR is the weakest. We note that though PRP is the best security notion one can hope to achieve for FPEs, the three weaker notions can, in many concrete cases offer much better efficiency and may therefore suffice in practice. Most of the schemes in practice focus on MP or MR security guarantees.

# .2 Proof of Thm. 1

Proof. For all $x \in \mathcal { X }$ and $i \in [ k ]$ , we have

$$
\frac {\Pr \left[ \mathcal {M} _ {\epsilon} (x , \epsilon) = i \right]}{\Pr \left[ \mathcal {M} _ {\epsilon} (x + t , \epsilon) = i \right]} =
$$

$$
\begin{array}{l} \left(e ^ {(| x + t - i | - | x - i |) \cdot \epsilon / 2} \cdot \frac {\sum_ {j = 1} ^ {k} e ^ {- | x + t - j | \cdot \epsilon / 2}}{\sum_ {j = 1} ^ {k} e ^ {- | x - j | \cdot \epsilon / 2}}\right) \\ \leq e ^ {t \epsilon / 2} \cdot e ^ {t \epsilon / 2} \\ [ \because | x - j | - t \leq | x + t - j | \leq | x - j | + t ] \\ = e ^ {t \epsilon} \tag {8} \\ \end{array}
$$

Similarly,

$$
\frac {\Pr \left[ \mathcal {M} _ {\epsilon} (x , \epsilon) = i \right]}{\Pr \left[ \mathcal {M} _ {\epsilon} (x + t , \epsilon) = i \right]} \geq e ^ {- t \epsilon}
$$

![](/image/Preempt/4d403db302c6e57a274c273067fb097cca562e1d5882bc64e67008fe226239fb.jpg)

# .3 Experimental Setup Details

# .3.1 Datasets

• Translation: Subsets of WMT-14 dataset for offline translation 7.   
• RAG: Simple GPT4-generated datasets for numerical comparisons and factual information retrieval.   
• Long-Context Q/A: Subsets of the NarrativeQA dataset.   
• Multi-Turn FinancialQ/A: We use the ConvFinQA dataset.   
• Named Entity Recognition: For fine-tuning NER model we use the AI4Privacy dataset (referred to as the PII dataset).

# .3.2 Frameworks and Infrastructure

• We use an implementation (pyfpe) of the FF3 algorithm [39] for format preserving encryption and a custom mLDP sanitization mechanism available in the provided code.   
• GPT-4o [80], Gemini-1.5 [45], and OPUS-MT [100] for translations, RAG, and question-answering tasks.   
• For NER we use Uni-NER [107], Llama-3 8B Instruct [2], and Gemma-2 9B Instruct [46] as open source models and GPT-4o[80] and Gemini 1.5[45] as closed source models.   
• 3 A100 GPUs for NER model fine-tuning, with the following configuration: half-precision (bfloat16), 16 gradient accumulation steps, learning rate of 2e-5, weight decay of 0, cosine learning rate schedule.

# .4 Impact on Utility (Q1)

# .4.1 Translation Task Details

For translation tasks we employ an LLM for NER of sensitive tokens belonging to the sensitive types of ([Name], [Age] and [Money]).

Name: Names are sanitized using FPE. We curate 1000 European first and last names using the First and Last Names Database [87]. Then for any full name found during NER, we have two cases: (1) the first and last names exist in our curated list or (2) they don’t, so we replace the last indices of each list with our found first and last names. Now, each name will have a certain index on the list between $0 0 0 - 9 9 9$ . Using both of these, we get a six digit number representing our found name. We can now apply standard FPE to obtain a new six digit number. The first three digits correspond to the index of the encrypted first name, and the last three digits correspond to the index of the encrypted last name. In case the found name is only a first (or last) name, we choose a default last (or first) name.

Money: Money is also sanitized using FPE. We simply add six “9”s to the front of the found monetary value and apply FPE. This also preserves any commas or spaces in the number. However, this does lead to some bizarre looking values such as $" 6 . 0 7 "$ being encrypted as “7728491.89”, which makes it difficult for NER to pick up.

Age: Age is sanitized over the domain of two digit numbers in integer increments[10, 11, . . . , 98, 99]; both settings employ an $\epsilon = 1$ . The sanitized prompt is submitted to an LLM for translation, and the NER model is again used to annotate the output text for desanitization.

To demonstrate the robustness of Prϵϵmpt, we use two modes of translation:

• Online models such as Gemini-1.5 [45] and GPT-4o [80]   
• Dedicated offline models like OPUS-MT [100]

To evaluate impact of sanitization on performance, we sample 50 English to German and English to French string pairs from the WMT-14 [14] dataset. As multiple translations can be valid and outputs of frontier models are not always deterministic, instead of testing for exact matches between desanitized translations of sanitized text translations of the original text, we compute BLEU scores to assess their respective similarities to reference translations.

# .4.2 Translation Results

We report the BLEU scores of translated plain text and Prϵϵmpt text (after desanitizing). We find that translation is largely invariant to prompt sanitization. This is true across different NER and translation models and different languages. Table 6 and Table 7 show results with different models for NER and a additional model for translation. We make the following observations:

1. We find there is only a marginal difference in the quality of plain and Prϵϵmpt translations across all types. We note that GPT-4o and Gemini-1.5 do sampling during text generation, thereby making their outputs nondeterministic. However, the plain and Prϵϵmpt translations are of high quality.   
2. We found a significant number of translations that are identical. However among the mismatched samples, we observed that translated sentence structures can vary due to the value of sanitized text, as shown in Figure 4 and Figure 5.   
3. We also note that the NER model would occasionally misidentify parts of the sensitive attribute. For example, if a monetary value was 121.445, it might only identify 121.4 as the sensitive attribute. This hinders performance during desanitization. However, we believe this can be solved with better finetuning and prompt engineering.

Language artifacts like these can make sanitation for exact translation difficult in practice. We leave a detailed analysis of this phenomena for future work.

We also note that Gemma-2 and Llama-3 as NER models don’t perfectly catch all PII values in the test samples. These samples are ignored while calculating BLEU scores. Specifically, the privacy leakage in terms of unique PII values missed are:

• Gemma-2: $4 . 8 \%$ on average, for both tasks.   
• Llama-3: $1 5 . 4 \%$ on average, for both tasks.

Additional Results at Higher Privacy Budgets: We present additional results for the translation task when considering ‘Age’ as the PII attribute in Fig. 3. We found a weak, but upward trend in BLEU scores with increasing values of $\epsilon$ (0.5 to 10), averaged across three different translation models and three seeds each. We believe that the signal is weak because the efficacy of translation is not critically dependent on the numerical value of the sensitive token considered here (‘Age’).

Performance of NER: NER performs better for English than for French and German. This impacts Prϵϵmpt’s utility, as desanitization involves running NER on the LLM’s response (translations in French and German).

Distribution of PII values: Since we want to measure the impact of sanitization on utility, we look up sanitized PII values for [Name] and [Money], instead of using NER in the desanitization phase. We found that $9 6 \%$ of all unique PII values were identified and sanitized by Prϵϵmpt, when using UniNER as the NER model. There are around 1.3 unique PII values per sentence on average, with around 1 instance per PII value in each sentence for both languages. More details regarding encryption and ablations can be found in App. .4.1 and App. .4.2.

# .4.3 Retrieval-Augmented Generation (RAG) Task Details

The aim of these experiments is to investigate if the sanitization of sensitive tokens of the following types – [Money], [CCN], [SSN], [ZipCode] and [Name] — impacts the correctness, and therefore utility of the LLM responses, in two types of question-answering scenarios: numerical comparisons, and retrieval of factual information.

Numerical Comparisons: We generate 20 tuples of Context, Questions and Answers using GPT4, where:

1. Context C is a few sentences describing financial details (jobs, salaries, credit debt, etc), which contain sensitive items like social-security numbers (SSN), credit-card numbers (CCN), salaries, credit-card balance.   
2. Question Q is a binary-choice comparison question, e.g. “Which credit card has higher balance?”   
3. Answer A is the correct answer, indicating choice 1 or 2. 8

![](/image/Preempt/cf6083a196e2412af7adac2e45e6b9caed62d6634cdf7194d2f4004a863ab016.jpg)

![](/image/Preempt/893737816ed6e0166301811dde237204a3513880633fa52b8f53e69fd40485a9.jpg)  
Figure 2: Median relative error for the Multi-turn Financial Q/A task, with increasing privacy budgets. We observe a consistent and smooth trend of median relative error (capturing utility of the model responses), improving with higher epsilon

![](/image/Preempt/d5431b012fff1b3ba33f32935ab275f90639cbe35da0d492e0713cdbd5cf40fe.jpg)  
(a) Translation: English German

![](/image/Preempt/fc329362e1065749623dadf905c089e0f3a166b4c7c1e53623a6d75cb8dfdf11.jpg)  
(b) Translation: English French   
Figure 3: Average BLEU scores for translation where the PII is ‘Age’, with increasing privacy budgets. We found that utility improves with larger values of $\epsilon$ .

For each such tuple C,Q, we apply Prϵϵmpt to sanitize the LLM input and desanitize the LLM response to compare with the correct answer A. We use GPT-4 to perform NER, FPE to sanitize [CCN], [SSN], [ZipCode] and [Name] and mLDP with $\epsilon = 1$ to sanitize [money] such as salaries and credit card balances. We sanitize C and Q jointly, i.e. copies of the same sensitive attribute across C and Q are updated using an LLM as well as verifying they are copies if they are both annotated as the same type and have the same value.

Retrieval of factual information We use GPT-4 to generate an e-commerce question/answering dataset consisting of 30 tuples. Each tuple consists of a Context C, Question Q and Answer A where:

1. Context is the description of customer orders, containing order IDs, cost, total cost with shipping, estimated arrival dates and shipping zip code.   
2. Question is a customer question about single aspect of their order (e.g. cost, estimated arrival etc)   
3. Answer is the correct response to the question, as a phrase.

Our procedure for applying Prϵϵmpt is the same as for numerical comparison tasks, with correctness evaluated by GPT-4.

Table 6: BLEU scores for the English German translation task, with different NER models. All scores are with respect to the reference translations from WMT-14.   

<table><tr><td colspan="7">Part A: UniNER-7B-PII</td></tr><tr><td rowspan="2">Attribute</td><td colspan="2">Gemini-1.5</td><td colspan="2">GPT-4o</td><td colspan="2">OPUS-MT</td></tr><tr><td>Plain</td><td>Preempt</td><td>Plain</td><td>Preempt</td><td>Plain</td><td>Preempt</td></tr><tr><td>Name</td><td>0.334</td><td>0.341</td><td>0.287</td><td>0.278</td><td>0.319</td><td>0.306</td></tr><tr><td>Age</td><td>0.235</td><td>0.252</td><td>0.243</td><td>0.231</td><td>0.294</td><td>0.282</td></tr><tr><td>Money</td><td>0.245</td><td>0.279</td><td>0.217</td><td>0.200</td><td>0.238</td><td>0.225</td></tr><tr><td colspan="7">Part B: Llama-3 8B Instruct</td></tr><tr><td>Name</td><td>0.338</td><td>0.304</td><td>0.292</td><td>0.265</td><td>0.319</td><td>0.297</td></tr><tr><td>Age</td><td>0.273</td><td>0.248</td><td>0.242</td><td>0.231</td><td>0.310</td><td>0.298</td></tr><tr><td>Money</td><td>0.256</td><td>0.269</td><td>0.219</td><td>0.193</td><td>0.238</td><td>0.228</td></tr><tr><td colspan="7">Part C: Gemma-2 9B Instruct</td></tr><tr><td>Name</td><td>0.336</td><td>0.307</td><td>0.292</td><td>0.258</td><td>0.319</td><td>0.303</td></tr><tr><td>Age</td><td>0.262</td><td>0.225</td><td>0.238</td><td>0.218</td><td>0.297</td><td>0.286</td></tr><tr><td>Money</td><td>0.260</td><td>0.243</td><td>0.219</td><td>0.193</td><td>0.238</td><td>0.223</td></tr></table>

Table 7: BLEU scores for the English French translation task, with different NER models. All scores are with respect to the reference translations from WMT-14.   

<table><tr><td colspan="7">Part A: UniNER-7B-PII</td></tr><tr><td rowspan="2">Attribute</td><td colspan="2">Gemini-1.5</td><td colspan="2">GPT-4o</td><td colspan="2">OPUS-MT</td></tr><tr><td>Plain</td><td>Preempt</td><td>Plain</td><td>Preempt</td><td>Plain</td><td>Preempt</td></tr><tr><td>Name</td><td>0.423</td><td>0.403</td><td>0.432</td><td>0.419</td><td>0.415</td><td>0.412</td></tr><tr><td>Age</td><td>0.486</td><td>0.490</td><td>0.480</td><td>0.479</td><td>0.470</td><td>0.471</td></tr><tr><td>Money</td><td>0.329</td><td>0.333</td><td>0.294</td><td>0.279</td><td>0.380</td><td>0.367</td></tr><tr><td colspan="7">Part B: Llama-3 8B Instruct</td></tr><tr><td>Name</td><td>0.428</td><td>0.365</td><td>0.432</td><td>0.365</td><td>0.415</td><td>0.373</td></tr><tr><td>Age</td><td>0.480</td><td>0.487</td><td>0.473</td><td>0.471</td><td>0.470</td><td>0.471</td></tr><tr><td>Money</td><td>0.353</td><td>0.353</td><td>0.297</td><td>0.282</td><td>0.380</td><td>0.359</td></tr><tr><td colspan="7">Part C: Gemma-2 9B Instruct</td></tr><tr><td>Name</td><td>0.407</td><td>0.381</td><td>0.430</td><td>0.361</td><td>0.415</td><td>0.363</td></tr><tr><td>Age</td><td>0.497</td><td>0.457</td><td>0.491</td><td>0.489</td><td>0.474</td><td>0.474</td></tr><tr><td>Money</td><td>0.330</td><td>0.330</td><td>0.307</td><td>0.282</td><td>0.380</td><td>0.360</td></tr></table>

# .4.4 RAG Results

We observe that our model achieves $1 0 0 \%$ accuracy for retrieval of factual information tasks and comparison tasks when using FPE as our encryption method.

# .4.5 Long-Context Q/A Task Details

We sanitize names using FPE, with the same process described in App. .4.1.

Failure Modes during NER: There are an average of 8.04 unique identities in each summary, and Prϵϵmptis able to correctly identify and sanitize $9 2 \%$ of all unique identities. There were instances where NER fails, particularly during the desanitization phase and our method’s performance decreases as a result. We found that when the name is more exotic (for example, “Co-tan”) NER will fail to pick it up. In fact, this extends to desanitization, where encrypted names tend to be exotic, such as “Paradise Arnoldo” and “Gheorghe Adamaene” are missed by NER. If there are ` two consecutive names (typically when a character is introduced, followed by the actor’s name in braces), NER will fail to pick up the second name. These are typically actor names mentioned only once and are not pertinent to the questions. Both models will occasionally misidentify titles such as “Count” or “the King” as valid names. They also occasionally misidentify pronouns (such as “him”, “she”) and articles (such as “the”) which are filtered accordingly. Lastly, UniNER occasionally hallucinates common names such as “Josh”, but these typically don’t occur in the summaries, so performance is unaffected.

Plain Text: She mastered go at 9 years old, became a professional go player at 14 in China and progressed to 2 dan at 16.

Plain Translation: Sie meisterte $\mathrm { \overline { { G } } O }$ mit 9 Jahren, wurde Profi-Go-Spieler mit 14 Jahren in China und erreichte mit 16 Jahren 2 Dan.

Sanitized Text: She mastered go at 11 years old, became a professonal go player at 14 in China and progressed to 2 dan at 16.

Encrypted Translation: Sie meisterte mit 11 Jahren das Go, wurde Profi-Gospielerin mit 14 Jahren in China und erreichte mit 16 Jahren 2 Dan.

Sanitized Text: She mastered go at 12 years old, became a professonal go player at 14 in China and progressed to 2 dan at 16.

Encrypted Translation: Sie meisterte $\mathrm { \Delta G O }$ mit 12 Jahren, wurde Profi-Go-Spielerin mit 14 Jahren in China und erreichte mit 16 Jahren 2 Dan.

Figure 4: Sanitized values can affect the grammatical structure of sentences. When we change a sensitive value like age from $\cdot 9 ^ { \cdot }$ in the plain text (highlighted in red), to ‘11’ in the sanitized text, the output translations also change (differences highlighted in blue). However, this occurs only for the number ‘11’ and returns to the original sentence structure if it is replaced with ‘12’ or any other value less than 100.Translation done using OPUS-MT, from English to German.

Plain Text: Parliament is now accepting the amendment of its proposal and will only be allowing ECU 150 million.

Plain Translation: Das Parlament akzeptiert jetzt die Anderung seines Vorschlags und wird nur 150 Millionen ECU zulassen.

Sanitied Text: Parliament is now accepting the amendment of its proposal and willonly be allowing ECU 110 million.

Encrypted Translation: Das Parlament akzeptiert jetzt die Anderung seines Vorschlags und wird nur 110 Millionen ECU zulassen.

Sanitized Text: Parliamentis now accepting the amendment of its proposal and willonly be allowing ECU 125 million.

Encrypted Translation: Das Parlament akzeptiert jetzt die Anderung seines Vorschlags und wird nur 125 Mio. ECU zulassen.

Sanitized Text: Parliament is now accepting the amendment of its proposal and willonly be allowing ECU 100 million.

Encrypted Translation: Das Parlament akzeptiert jetzt die Anderung seines Vorschlags und wird nur noch 100 Mio. ECU zulassen.

Sanitized Text: Parliament is now accepting the amendment of its proposal and willonly be allowing ECU 10 million.

Encrypted Translation:Das Parlament akzeptiert jetzt die Anderung seines Vorschlags und wird nur noch 10 Millionen ECU zulassen.

Figure 5: Changes in output translations for different sanitized values. As we see, the numerical money value (green) can change the words that come before and after it (blue). Translation done using OPUS-MT, from English to German.

Additional STS Scores for Prϵϵmpt: We report additional STS scores with respect to plain responses without desanitization (“Encrypted”), and irrelevant answers (“Irrelevant”) in Table 8. On average, we see that Prϵϵmpt is able to capture the semantics of the passage even with all PII values sanitized and maintains high utility with open and closed-source models. Without desanitization, the STS score falls dramatically for all Q/A models. If the answers are completely irrelevant then the scores drop to 0.15 on average, showing the robustness of the metric.

Table 8: Semantic Textual Similarity scores of different methods for the Long-Context Q/A task. Higher value implies more similarity with the reference answer. “Plain Responses” refer to the responses for unsanitized inputs. “References” indicate the ground truth responses. “Encrypted” indicates the STS scores of Prϵϵmpt responses without desanitization, with respect to the plain responses. Lastly, “Irrelevant” refers to the STS scores with an irrelevant reference answer. We find that Prϵϵmpt has a particularly high utility with respect to GPT-4o, outperforming prior methods. Prϵϵmpt uses Gemma-2 9B Instruct as the NER model Gemini-1.5 and UniNER for Llama-3 and GPT-4o.

<table><tr><td>STS Score</td><td>Llama-3</td><td>Preempt Gemini-1.5</td><td>GPT-4o</td><td>Papillon GPT-4o</td></tr><tr><td>Plain Responses</td><td>0.839</td><td>0.849</td><td>0.934</td><td>0.854</td></tr><tr><td>References (GT)</td><td>0.514</td><td>0.722</td><td>0.510</td><td>0.458</td></tr><tr><td>Encrypted</td><td>0.450</td><td>0.496</td><td>0.523</td><td>-</td></tr><tr><td>Irrelevant</td><td>0.148</td><td>0.166</td><td>0.146</td><td>0.141</td></tr></table>

# .4.6 Additional Results for Multi-Turn Financial Q/A

We include additional results for this task when considering a broad range of privacy budgets in Fig. 2. We observe a consistent and smooth trend of median relative error (capturing utility of the model responses), improving with higher ϵ (0.5 to 5). The Financial Q/A dataset primarily consists of numerical reasoning and retrieval, making its utility much more sensitive to the amount of noise present; as long as the model’s underlying reasoning is correct, the amount of noise would have a direct functional relationship with the relative error, explaining the consistent and smooth improvements.

# .5 Comparison with Prior Methods (Q2)

# .5.1 Comparison with Strawman Solutions

Redaction: For example, consider a factual information retrieval task in the context of RAG for financial documents, with the prompt: “Please return all bank accounts with balance greater than $\$ 2000$ .” If the sensitive tokens of the types [Bank A/c] or [Bank Balance] are redacted, the LLM is unable to provide any useful response. Furthermore, any tasks which rely on operations over sensitive information, such as numerical reasoning, would similarly provide little to no utility, even if redacted tokens are replaced by a ”best guess” of a masked language model.

# .5.2 Translation Task - Papillon

We made a few observations about Papillon that could explain its worse performance. Firstly, the remote model frequently outputs a lot of extra text, such as the input English sentence, which reduces the score. The local model also occasionally includes new text, or misinterprets the user instruction as part of the created prompt. We report our results after cleaning up redundant text and not counting samples with egregious errors, such as the user instruction being ignored. Secondly, the optimized prompts found by Papillon tend to focus on the content of the finetuning data. In this case, the data comes from WMT-14 and is political in nature. As a result, the optimized prompt emphasizes this, and the prompt creator loses performance. We present some examples of the errors produced by Papillon:

User Instruction Ignored: This results in several extra lines being produced by the remote model that are not related to the translation task:

• User Query: “Please translate this sentence into German: Today, minors are being sentenced to death in Iran and one, Ateqeh Rajabi, aged 16, has been hanged.”   
• Papillon Created Prompt: “Please provide information on international legal policies regarding the sentencing of minors to death, including any notable cases or countries where such practices have been observed. Focus on the general trends, laws, and regulations surrounding this issue, without referencing specific individuals or cases.”   
• Papillon Response: “Heute werden Minderjahrige in Iran zum Tode verurteilt, und eine 16-j ¨ ahrige Frau ¨ namens Ateqeh Rajabi wurde gehangt. ¨

Die internationale Rechtslage bezuglich der Todesstrafe f ¨ ur Minderj ¨ ahrige hat sich in den letzten Jahren ¨ erheblich verandert, mit einem starken globalen Trend hin zur Abschaffung dieser Praxis.¨

Die wichtigsten Punkte und Trends sind:

1. **Internationale Menschenrechtsstandards**: - Die Vereinten Nationen-Konvention uber die Rechte ¨ des Kindes (CRC), die von fast jedem Land ratifiziert wurde, verbietet ausdrucklich die Anwendung der ¨ Todesstrafe fur Vergehen, die von Personen unter 18 Jahren begangen wurden. ¨   
5. **Befurworter und Reformbem ¨ uhungen**: - Internationale Organisationen wie Amnesty International¨ und Human Rights Watch kampfen gegen die ¨

Insgesamt bevorzugt die internationale Rechtslandschaft die Abschaffung der Todesstrafe fur Minderj ¨ ahrige, ¨ mit laufenden Bemuhungen, um mit den internationalen Menschenrechtsstandards ¨ ubereinzukommen. Der¨ Trend geht in Richtung universeller Abschaffung, obwohl Herausforderungen in bestimmten Gerichtsbarkeiten bestehen bleiben.”

# English Input Sentence Included as part of Output:

• User Query: “Please translate this sentence into French: It goes back, though, to a time when EUR 58.5 billion more was meant to be allocated to Category 1A.”   
• Papillon Created Prompt: “Please translate the following sentence into French, replacing any sensitive information with the following placeholders: [AMOUNT] for monetary values and [CATEGORY] for category names. The sentence is: It goes back, though, to a time when [AMOUNT] more was meant to be allocated to [CATEGORY].”   
• Papillon Response: “It goes back, though, to a time when EUR 58.5 billion more was meant to be allocated to Category 1A. translates to: Cela remonte, cependant, a une ` epoque o ´ u 58,5 milliards d’euros de plus ` devait etre allouˆ e´ a la cat` egorie 1A.”´

# .5.3 Long-Context Q/A Task - Papillon

Prϵϵmpt is able to sanitize $9 2 \%$ of all unique character identities found across all samples, whereas Papillon (by omission) is able to sanitize $8 8 \%$ queries. We found that in $8 0 \%$ of cases, Papillon ended up passing character identities to the remote model. For example:

• User Query: “Please answer the question based on the summary. Be as concise as possible.

# SUMMARY:

Maskull, a man longing for adventures, accepts an invitation from Krag, an acquaintance of his friend Nightspore, to travel to Tormance after a seance. The three ...”

• Papillon Created Prompt: “Please describe the social connection between Krag and Nightspore’s friend, highlighting the nature of their relationship and any notable interactions between them.”

Here is an example where character identity is successfully omitted:

• User Query: “Please answer the question based on the summary. Be as concise as possible.

# SUMMARY:

The story follows its title heroine, from childhood to confirmation. After her mother’s death, Lisbeth (given the nickname Longskirt, or SidsA˘ Srk in the original Norwegian, because of her much too-long skirt, a Christ-´ mas present given her by her brother) as ...”

• Papillon Created Prompt: “Please describe the title heroine’s family members, including their names and relationships to her. What are the names of her parents and siblings, and what are their roles in the story?”

# .6 Impact of Technical Design Choices (Q3)

# .6.1 Named Entity Recognition (NER)

We ablate translation experiments over 6 NER models. We finetune the Uni-NER model for two epochs on 70K positive samples (where the model is prompted to return empty lists for irrelevant entities) from the AI4Privacy dataset [1] containing 54 classes of personally identifiable information including named entities of our interest (Name, Age, Money, CCN, SSN, ZipCode, Date, Password, Sex and Phone Number). The data is split roughly equally between

three languages: English, German and French. We compare its performance against 5 other models on a held out subset of the AI4Privacy dataset consisting of 50 samples of each attribute of interest across all three languages. We present the results of NER in Table 4.

Prompt template for NER Used in experiments pertaining to Table 4 for different sensitive attributes:

1. Name: “Please find words that can be identified as names of people from the given text. Format the output as a dictionary of lists: {‘Name’: [‘Name 1’, ‘Name 2’]}. Do NOT provide any additional text.”   
2. Money: “Please find currency values from the given text. Do not provide the currency, only provide the value, WITHOUT changing commas or decimal points. Format the output as a dictionary of lists: $\{ \mathsf { \Omega } \cdot \mathsf { M o n e y } ^ { \prime }$ : [‘Money 1’, ‘Money 2’]}. Do NOT provide any additional text.”   
3. Other: “Please find words that can be identified as ‘entity’ from the given text. Format the output as a dictionary of lists: {‘entity’: [‘entity 1’, ‘entity 2’]}. Do NOT provide any additional text.”

# .6.2 Encryption Format

To assess the importance of format preservation of sanitization methods on model utility, we examine them in the context of RAG Question Answering. We generate 31 tuples of context C, question Q and answers A, using GPT4, where the questions amount to retrieval of sensitive information from the context (e.g. credit card number, date of purchase etc.). For each tuple C,Q,A, we compare Format Preserving Encryption and AES Encryption for sanitizing sensitive attributes and evaluate percentage of correct, desanitized, answers using GPT4. To compare against less drastic formatting changes, we also evaluate substituting sensitive attributes with a random string that does not match the format of the sensitive attribute (for example, a 5-digit zipcode can be changed to a randomly chosen 4-digit or 8-digit value). Desanitization is performed using a local lookup table created during sanitization.

# .6.3 Results for Technical Design Choices

Named Entity Recognition: As seen in Table 4, our fine tuned Uni-NER model outperforms all other 5 models. We use a general prompt template (provided above) for these models where we ask them to return instances of a given entity in a list form. The performance of closed-source models could be improved with better prompt engineering. For example, the score for [Name] is typically lower because these models frequently pick up company names and email-IDs as part of NER. We believe proper prompt engineering will improve the NER performance of these models in general and we leave it as future work.

Encryption Format: We observe that our model achieves $100 \%$ accuracy in factual information retrieval when employing Format Preserving Encryption. However, performance drops to $7 0 . 9 7 \%$ with AES encryption and $7 7 . 4 2 \%$ with random substitution using incorrect formats. This confirms our assumption that preserving the format is crucial for maintaining the LLM’s performance.

# .7 Additional Examples of the Helper String

We present some additional scenarios where the helper string is crucial for high utility:

Example 1 Prompt: “My age is X, I was born in Y. I am X years old.”

This prompt contains three sensitive tokens:[Age-X],[Year-Y] and [Age-X]. By default, Prϵϵmpt distributes the privacy budget equally $( \epsilon / 3 )$ among all type-II tokens(Alg. 2). This ensures an overall $\epsilon$ -mDP guarantee across all type-II tokens through composition.

However, we achieve a better privacy-utility trade-off by leveraging the helper string $\Psi$ , which encodes additional information about token relationships, such as correlations. E.g., $\Psi$ can indicate that X and Y represent the same ground-truth and that X appears twice in the prompt. Using this information, Prϵϵmpt applies $\epsilon$ -mDP to the first occurrence of X, generating $\hat { X }$ .

Suppose $\hat { X } = 2 5$ ; Prϵϵmpt then derives the corresponding $\hat { Y } = 2 0 0 0$ by post-processing and reuses $\hat { X }$ for the second occurrence of age.This incurs no additional privacy loss due to the post-processing immunity of mDP [35].

Example 2 Prompt:“My monthly salary is X and my yearly salary is Y and I have Q in annual deductions. My annual taxable income is Z”

This prompt contains four sensitive tokens: [Monthly Salary, X], [Yearly Salary, Y], [Annual Deductions, Q], and [Taxable Income, Z].

These tokens are related by the following constraints:

1. $\mathrm { Y } = 1 2 \times \mathrm { X }$ (yearly salary is 12 times monthly salary)   
2. $\boldsymbol { { Z } } = \mathbf { Y } - \boldsymbol { { Q } }$ (taxable income equals yearly salary minus deductions)

Using the helper string $\Psi$ , Prϵϵmpt can encode these relationships. For example, if:

• $\mathbf { X } = \mathbb { \ S } 5 , 0 0 0$ (original monthly salary)   
• $\mathrm { Y } = \mathfrak { F } 6 0 , 0 0 0$ (original yearly salary)   
• $\mathrm { Q } = \mathfrak { H } 1 0 , 0 0 0$ (original deductions)   
• $\mathsf { Z } = \$ 50,000$ (original taxable income)

Prϵϵmpt would:

1. Apply $\epsilon / 2 \mathrm { - m D P }$ $\epsilon / 2$ to X, generating $\hat { X }$ (e.g., $\hat { X } = \$ 5,200 )$   
2. Derive $\hat { Y } = 1 2 \hat { X } = \mathbb { \ S } 6 2 ,$ 400 through post-processing   
3. Apply $\epsilon / 2$ -mDP to Q, generating $\hat { Q }$ (e.g., $\hat { Q } = \mathfrak { F } 9 , 8 0 0 )$   
4. Derive $\hat { Z } = \hat { Y } - \hat { Q } { = } \mathfrak { H } 5 2 , 6 0 0$ through post-processing

Sanitized prompt:“My monthly salary is $\$ 5$ , 200 and my yearly salary is $62, 400 and I have $\$ 9$ , 800 in annual deductions. My annual taxable income is $52, 600”

# .8 Robustness to Adversaries

In this section, we elaborate on the security guarantees provided by Prϵϵmpt against adversaries for both types of sanitized tokens.

Category I tokens These are protected via the cryptographic guarantee of the underlying FPE scheme as captured our game-based security definition Sec. 3.1.Our FPE scheme provides Pseudo-Random Permutation security [13]–the strongest guarantee for a FPE scheme,ensuring that an adversary cannot distinguish encryptions with a random key from random permutations over the format domain.

Category II tokens These are protected by metricDP. Standard DP would result in catastrophic utility loss in our setting; metricDP is a well-established relaxation in the privacy literature [57, 23, 5, 41, 30] that balances the privacy/utility tradeoff. It is also the standard approach for ensuring privacy in NLP tasks [76, 42, 24, 21]. Reverseengineering attacks are mitigated by the post-processing immunity of metricDP, which ensures that any transformation applied to the sanitized tokens incurs no additional privacy loss.

We do not make any assumptions about the adversary’s capabilities, except that it is probabilistic-polynomial-time (as required by cryptographic primitives). Prϵϵmpt is resilient against reverse-engineering attacks that rely solely on sanitized tokens. As noted earlier, contextual privacy leakage is out-of-scope.

# .9 Open Problems and Discussion

Automated Discovery of Token Dependencies: For maximum utility, the encryption space for sensitive tokens should be domain-constrained, preserving the context and relationships between tokens. For example, if “Paris” and “France” are sensitive in “Paris is the capital of France,” they should be replaced with another city-country pair, such as “Rome is the capital of Italy,” to maintain the “capital city” relationship. In the current version of Prϵϵmpt, users must specify relationship constraints using a helper string. While LLMs can infer complex relationships ([51, 104]), doing so unsupervised is challenging, especially for subtle or implied connections. These relationships may also vary or conflict across different sensitive tokens. We are exploring solutions to these challenges for future versions of Prϵϵmpt.

Encoding Token Dependencies: Once we discover the relationship between different sets of sensitive tokens, we now have to meaningfully constrain the encryption space for those tokens. For example, consider the sentence, “of his regular income of $\$ 5000$ , he always saved $\$ 500$ , (as part of a larger prompt) and suppose the two sensitive attributes are “ $\$ 500$ and $\mathfrak { s } 5 0 0 0 ^ { \mathfrak { s } }$ . Given the context, a user (through a helper string) or a LLM will infer the relationship to be “ $\mathrm { \dot { 2 } 0 \% }$ of”. Once we have this information, we must use it to constrain the encryption space such that whatever $\mathfrak { s o o o } \mathfrak { s } 5 0 0 0 ^ { \mathfrak { s } }$ gets encrypted as, $\mathfrak { s } 5 0 0 ^ { \mathfrak { s } }$ gets encrypted keeping the plaintext relationship in mind. It is not clear how this is practically accomplished, especially for more open-ended mappings or non-numerical relationships.

Critical Dependence for Utility: There are a certain set of prompts that are critically dependent on the sensitive attribute for their utility. For example, it might be a product code that you are inquiring about. Any change to the number during sanitization would misdirect the LLM agent to some other product and utility is lost. In this case, the user can provide a helper string indicating that a particular token is to be ignored during sanitization. Automating this is important, as the user can’t be expected to provide all such exceptions.

Very Small Integer Domains for FPE: We found that the domains of many common sensitive attributes tend to be very small, with respect to FPE schemes. For example, if a country name was determined to be a sensitive attribute, it can only be replaced from a list of 195 internationally recognized countries. In such a case, FPE cannot be applied and other methods must be considered. This can be the case for other niche domains. Mechanisms like mLDP with a unique distance metric defined for these domains might be a viable solution.

Inferring Sensitive Information from Context: Prϵϵmpt focuses solely on the privacy concerns stemming from the individual tokens: it does not address the privacy risks that arise when the entire context of the prompt is considered. For example, while tokens like “neighbor,” “abusive,” and “marriage” are not sensitive individually, the full prompt “My neighbor is in an abusive marriage” is sensitive. Designing prompt sanitizers that prevent leakage of such contextual information remains an open challenge. Assessing privacy risk is complex and context-dependent, requiring: (1) identifying safe contexts for sharing, (2) defining what constitutes a secret, and (3) knowing who already has access to that information [16]. Another challenge lies in creating a general-purpose sanitization mechanism that consistently yields good utility, regardless of downstream task specification, as it’s not feasible to make a custom mechanism for each task.

# .10 Proof of Theorem 2

The proothe game in two stages. First, w where the two prompts how and elper resudiffer in that shows that the advantage of the adversary sensitive tokens is upper bounded by the sum o $\mathcal { A }$ inthe $\mathbf { G } _ { \mathsf { P S } , \mathcal { L } } ^ { \mathrm { p p } }$ $\pmb { \rho } _ { 0 }$ $\pmb { \rho } _ { 1 }$ $k$ advantage of $k$ individual games corresponding to the $k$ sensitive tokens. Next, we give a bound on the adversary’s advantage when $\rho _ { 0 }$ and $\pmb { \rho } _ { 1 }$ differ only in a single token under Prϵϵmpt. The final result can be obtained by combing the above results.

Helper Result. For this, we instantiate the leakage function using an equivalence relation. We assume that there is an equivalence relation $R : V ^ { \star } \times V ^ { \star }$ (intuitively, $( \pmb { \rho } _ { 0 } , \pmb { \rho } _ { 1 } ) \in R$ means that the prompts $\rho _ { 0 }$ and $\pmb { \rho } _ { 1 }$ are ”equivalent”). 0 1 0Two prompts are said to be equivalent if they have the same leakage: we denote the advantage as $\mathbf { A d v } _ { \mathsf { P S } , R } ^ { \mathrm { p p } ^ { - } } ( { \cal A } )$ . We assume that the equivalence relation preserves types (i.e. $( \pmb { \rho } _ { 0 } , \pmb { \rho } _ { 1 } ) \in R$ implies that $\rho _ { 0 }$ and $\pmb { \rho } _ { 1 }$ have the same type).

Note that the sources of randomness in the game come from the scheme and the adversary. We now derive an alternative expression for the advantage which sometimes easier to work with. Splitting on the random variable $b$ we can write the following sequence of expressions:

$$
\begin{array}{l} 2 \Pr \left[ \mathbf {G} _ {\mathrm {P S}, R} ^ {\mathrm {p p}} (\mathcal {A}) = 1 \right] - 1 \\ = \left| P \left(\boldsymbol {\rho} _ {0}, \boldsymbol {\rho} _ {1}, b ^ {\prime} = 0 \mid b = 0\right) + P \left(\boldsymbol {\rho} _ {0}, \boldsymbol {\rho} _ {1}, b ^ {\prime} = 1 \mid b = 1\right) - 1 \right| \\ = \left| P \left(\boldsymbol {\rho} _ {0}, \boldsymbol {\rho} _ {1}, b ^ {\prime} = 0 \mid b = 0\right) - P \left(\boldsymbol {\rho} _ {0}, \boldsymbol {\rho} _ {1}, b ^ {\prime} = 0 \mid b = 1\right) \right| \\ \end{array}
$$

Next we discuss some specific equivalence relations $R$ . Consider an equivalence relation $R _ { k , \{ t _ { 1 } , \cdots , t _ { k } \} }$ as follows: $( \pmb { \rho } , \pmb { \rho } ^ { \prime } ) \in R _ { k , \{ t _ { 1 } , \cdots , t _ { k } \} }$ iff types of $\rho$ and $\rho ^ { \prime }$ are the same and the two prompts only differ in at most $k$ sensitive tokens whose types are $\{ t _ { 1 } , \cdots , t _ { k } \}$ , which we formalize next. Let $\pmb { \rho } _ { \tau } = ( \pmb { \rho } , \langle ( \sigma _ { 1 } , \tau _ { 1 } ) , \cdot \cdot \cdot , ( \sigma _ { n } , \tau _ { n } ) \rangle )$ , and $\pmb { \rho } _ { \tau } ^ { \prime } =$ $( \pmb { \sigma } ^ { \prime } , \langle ( \sigma _ { 1 } ^ { \prime } , \tau _ { 1 } ) , \cdots , ( \sigma _ { n } ^ { \prime } , \acute { \tau _ { n } } ) \rangle )$ ). We assume that there are $k$ distinct indices $I = \{ i _ { 1 } , \cdots , i _ { k } \}$ such that $\sigma _ { j } \neq \sigma _ { j } ^ { \prime }$ iff $j \in I$ and $\tau _ { j } \neq \bot$ and, moreover the types of tokens corresponding to indices in $I$ are $\{ t _ { 1 } , \cdots , t _ { k } \}$ .

Next we focus on the equivalence relation $R _ { 1 , t }$ , or the game ${ \bf G } _ { \mathsf { P S } , R _ { 1 , t } } ^ { \mathrm { p p } }$ . Suppose adversary $A$ picks two prompts $\rho _ { 0 }$ and $\pmb { \rho } _ { 1 }$ in $\vee ^ { * }$ such that they only differ in one token at index $i$ and the type of that token is $t$ . We have the following

system of equations:

$$
\begin{array}{l} \mathbf {A d v} _ {\mathsf {P S}, R _ {1, t}} ^ {\mathrm {p p}} (\mathcal {A}) \\ = \left| P \left(\boldsymbol {\rho} _ {0}, \boldsymbol {\rho} _ {1}, b ^ {\prime} = 0 \mid b = 0\right) - P \left(\boldsymbol {\rho} _ {0}, \boldsymbol {\rho} _ {1}, b ^ {\prime} = 0 \mid b = 1\right) \right| \\ = \left| P \left(\boldsymbol {\rho} ^ {\prime}\right) \left[ P \left(\boldsymbol {\sigma} _ {0}, \boldsymbol {\sigma} _ {1}, b ^ {\prime} = 0 \mid \boldsymbol {\rho} ^ {\prime}, b = 0\right) \right. \right. \\ - P \left(\sigma_ {0}, \sigma_ {1}, b ^ {\prime} = 0 \mid \rho^ {\prime}, b = 1\right) ] \\ \end{array}
$$

In the equation given above, $\rho _ { 0 }$ is constructed by inserting token $\pmb { \sigma } _ { 0 }$ in index $i$ of $\rho ^ { \prime }$ , and $\pmb { \rho } _ { 1 }$ is constructed by inserting token $\pmb { \sigma } _ { 1 }$ in index $i$ of $\rho ^ { \prime }$ (here we are leveraging that $\rho _ { 0 }$ and $\pmb { \rho } _ { 1 }$ only differ in one token and whose type is $t$ ). Now assume that $\mathbf { A d v } _ { \mathsf { P S } , R _ { 1 , t } } ^ { \mathrm { p p } } ( \mathcal { A } )$ is $\geq \epsilon$ 0 1 . This means that there exists one specific $\rho ^ { \prime }$ such that rhs of the second equation is $\geq \epsilon$ . In other words, we can limit ourselves to an adversary that picks $\pmb { \sigma } ^ { \prime }$ deterministically, and only picks $\pmb { \sigma } _ { 0 }$ and $s s _ { 1 }$ randomly given $\rho ^ { \prime }$ .

Single token game. Consider the game ${ \bf G } _ { \mathsf { P S } , t } ^ { \mathrm { p p } }$ , which corresponds to adversary picking two tokens $\pmb { \sigma } _ { 0 }$ and $\pmb { \sigma } _ { 1 }$ of type $t$ . For the sake of completeness, we describe this game. Our game ${ \bf G } _ { \mathsf { P S } , t } ^ { \mathrm { p p } }$ is played between the adversary $\mathcal { A }$ and the sanitization mechanism PS.

1. Adversary $\mathcal { A }$ picks two tokens of type $\pmb { \sigma } _ { 0 }$ and $\pmb { \sigma } _ { 1 }$ of type $t$ .   
2. $\mathcal { A }$ sends $\pmb { \sigma } _ { 0 }$ and $\pmb { \sigma } _ { 1 }$ to the mechanism PS, which flips a random coin $b  { } _ { r } \{ 0 , 1 \}$ and sends the sanitized token $\pmb { \sigma } _ { b } ^ { \prime }$ to the adversary.   
3. Adversary guesses $b ^ { \prime }$ and wins if their guess is correct (i.e. $b = b ^ { \prime }$ ). If the adversary wins, the game’s outputs 1; otherwise the game’s outputs 0

As usual, the advantage of the game (denoted as $\mathbf { A d v } _ { \mathsf { P S } , t } ^ { \operatorname { p p } } ( { \mathcal { A } } ) )$ is defined as

$$
\mid 2 P r [ \mathbf {G} _ {\mathsf {P S}, t} ^ {\mathrm {p p}} (\mathcal {A}) = 1 ] - 1 \mid
$$

The following inequality is easy to prove:

$$
\mathbf {A d v} _ {\mathsf {P S}, t} ^ {\mathrm {p p}} (\mathcal {A}) \geq \mathbf {A d v} _ {\mathsf {P S}, R _ {1, t}} ^ {\mathrm {p p}} (\mathcal {A}) \tag {9}
$$

The argument goes as follows: consider an adversary $A ^ { \prime }$ for the game corresponding to the equivalence relation $R _ { 1 , t }$ (recall that $A ^ { \prime }$ picks $\pmb { \sigma } ^ { \prime }$ deterministically, picks two tokens $v _ { 0 } \ v _ { 1 }$ randomly). Since $\rho ^ { \prime }$ is deterministic it can be viewed as an argument to adversary $A$ for the game $A d v ( S e c _ { A , \mathsf { P S } , t } )$ , and the inequality follows.

Now we turn to the equivalence relation $R _ { k , \{ t _ { 1 } , \cdots , t _ { k } \} }$ introduced earlier. Recall that the equivalence relation is defined as follows: $( \pmb { \rho } , \pmb { \rho } ^ { \prime } ) \in R _ { k , \{ t _ { 1 } , \cdots , t _ { k } \} }$ iff types of $\rho$ and $\rho ^ { \prime }$ are same and the two prompts only differ in at most $k$ sensitive tokens whose types are $\{ t _ { 1 } , \cdots , t _ { k } \}$ , which we formalize next. We assume that there are $k$ distinct indices $I \ =$ $\{ i _ { 1 } , \cdots , i _ { k } \}$ such that $\pmb { \sigma } _ { j } \neq \pmb { \sigma } _ { j } ^ { \prime }$ iff $j \in I$ and $\tau _ { j } \neq \bot$ , and the types of tokens corresponding to indices in $I$ is $\{ t _ { 1 } , \cdots , t _ { k } \}$ . Given two strings $\pmb { \rho } _ { 0 }$ and $\pmb { \rho } _ { 1 }$ we define a sequence of strings $\rho ^ { 0 } , \rho ^ { 1 } , \rho ^ { 2 } , \cdots , \rho ^ { j }$ inductively as follows: $\rho ^ { 0 } = \rho _ { 0 }$ , and for $1 \leq j \leq k$ define $\rho ^ { j }$ as $\pmb { \rho } ^ { j - 1 }$ with token at index $i _ { j }$ changed to the $i _ { j }$ -th token of $\pmb { \rho } _ { 1 }$ . Note that $\rho ^ { k } = \rho _ { 1 }$ . Essentially we change one token at a time, starting from $\rho _ { 0 }$ . One key observation is that $\rho ^ { j }$ and $\rho ^ { j + 1 }$ only differ in one token.

Consider the following equation for the advantage:

$$
\begin{array}{l} \mathbf {A d v} _ {\mathsf {P S}, R _ {k, \{t _ {1}, \dots , t _ {k} \}}} ^ {\mathrm {p p}} (\mathcal {A}) \\ = \left| P r \left[ \boldsymbol {\rho} _ {0}, \boldsymbol {\rho} _ {1}, b ^ {\prime} = 0 \mid b = 0 \right] - P r \left[ \boldsymbol {\rho} _ {0}, \boldsymbol {\rho} _ {1}, b ^ {\prime} = 0 \mid b = 1 \right] \right. \\ \end{array}
$$

Let $D ^ { 0 }$ be the distribution corresponding to adversary picking the prompts $\rho _ { 0 } , \rho _ { 1 }$ and the scheme PS sanitizing $\rho _ { 0 }$ . Let $D ^ { k + 1 }$ be the distribution corresponding to adversary picking the prompts $\rho _ { 0 } , \rho _ { 1 } .$ and scheme sanitizing $\pmb { \rho } _ { 1 }$ . Now we create a distribution $D ^ { j }$ $1 \leq j \leq k )$ as follows: this corresponds to the prompts $\rho ^ { j }$ , $\rho ^ { j + 1 }$ and the scheme sanitizing

$\rho ^ { j }$ . Note that we can write the advantage as:

$$
\begin{array}{l} \mathbf {A d v} _ {\mathsf {P S}, R _ {k, \{t _ {1}, \dots , t _ {k} \}}} ^ {\mathrm {p p}} (\mathcal {A}) \\ = \left| P r \left[ x \leftarrow^ {R} D ^ {0}: \mathcal {A} (x) = 0 \right] - P r \left[ x \leftarrow^ {R} D ^ {k + 1}: \mathcal {A} (x) = 0 \right] \right| \\ \leq \sum_ {i = 1} ^ {k} | P r [ x \leftarrow^ {R} D ^ {i - 1}: \mathcal {A} (x) = 0 ] - P r [ x \leftarrow^ {R} D ^ {i}: \mathcal {A} (x) = 0 ] | \\ \leq \sum_ {i = 1} ^ {k} \mathbf {A d v} _ {\mathrm {P S}, R _ {1, t _ {i}}} ^ {\mathrm {p p}} (\mathcal {A}) \\ \leq \sum_ {i = 1} ^ {k} \mathbf {A d v} _ {\mathrm {P S}, t} ^ {\mathrm {p p}} (\mathcal {A}) \tag {10} \\ \end{array}
$$

The penultimate step follows from triangle inequality, and the last step follows from the inequality proved earlier. In words, the advantage of the game where multiple tokens can change is upper bounded by the advantage of the game corresponding to the individual tokens. Recall that this is the standard hybrid argument used in security.

Analyzing single token game. Now we turn to $A d v ( S e c _ { A , \mathsf { P S } , t , L } )$ which depends on the type $t$ of the sensitive attribute.

t corresponds to $\tau _ { \bar { I } }$ . In this case the advantage is negligible function in the security parameter or $n e g l ( \kappa )$ , which follows from the security of the FPE scheme (App. .1).

t corresponds to using $\tau _ { T \bar { I } }$

Advantage of adversary for mLDP: Denoting $p _ { 0 } = \mathrm { P r } [ b ^ { \prime } = b \mid b = 0 ]$ and $p _ { 1 } = \mathrm { P r } [ b ^ { \prime } = b \mid b = 1 ]$ , we have

$$
\operatorname * {P r} [ b ^ {\prime} = b ] = \frac {1}{2} p _ {0} + \frac {1}{2} p _ {1}
$$

mLDP and the associated composition theorem ensures that

$$
\Pr \left[ \mathsf {E} \left(\boldsymbol {\rho} _ {0}\right) = \boldsymbol {\rho} _ {c} ^ {\prime} \right] \leq e ^ {\epsilon d \left(\boldsymbol {\rho} _ {0}, \boldsymbol {\rho} _ {1}\right)} \Pr \left[ \mathsf {E} \left(\boldsymbol {\rho} _ {1}\right) = \boldsymbol {\rho} _ {c} ^ {\prime} \right]
$$

Note that we drop the key and $\scriptstyle { \mathcal { M } } _ { \tau } ( \rho )$ from the expression $\mathsf E ( \rho _ { 0 } )$ above for ease of notation. Due to the postprocessing inequality, as the adversary guess $b ^ { \prime }$ is a function of $\pmb { \sigma } _ { c } ^ { \prime }$ , this can be translated as

$$
\Pr \left[ b ^ {\prime} = b \mid \mathsf {E} \left(\rho_ {0}\right) \right] \leq e ^ {e d \left(\rho_ {0}, \rho_ {1}\right)} \Pr \left[ b ^ {\prime} = b \mid \mathsf {E} \left(\rho_ {1}\right) \right]
$$

Then,

$$
\begin{array}{l} \Pr \left[ b ^ {\prime} = b \right] = \frac {1}{2} \Pr \left[ b ^ {\prime} = b \mid \mathsf {E} \left(\boldsymbol {\rho} _ {0}\right) \right] + \frac {1}{2} \Pr \left[ b ^ {\prime} = b \mid \mathsf {E} \left(\boldsymbol {\rho} _ {1}\right) \right] \\ \leq \frac {1}{2} e ^ {\epsilon d (\boldsymbol {\rho} _ {0}, \boldsymbol {\rho} _ {1})} \Pr [ b ^ {\prime} = b \mid \mathsf {E} (\boldsymbol {\rho} _ {1}) ] + \frac {1}{2} \Pr [ b ^ {\prime} = b \mid \mathsf {E} (\boldsymbol {\rho} _ {1}) ] \\ = \Pr [ b ^ {\prime} = b \mid \mathsf {E} (\boldsymbol {\rho} _ {1}) ] \frac {1}{2} (e ^ {\epsilon d (\boldsymbol {\rho} _ {0}, \boldsymbol {\rho} _ {1})} + 1) \\ \leq \frac {1}{2} + \frac {e ^ {\epsilon d \left(\boldsymbol {\rho} _ {0} , \boldsymbol {\rho} _ {1}\right)}}{2} \tag {11} \\ \end{array}
$$

Recall that $\operatorname* { P r } [ b ^ { \prime } = b ]$ corresponds to the adversary winning the game, and thus the advantage can be easily computed as $e ^ { \epsilon d ( \pmb { \sigma } _ { 0 } , \pmb { \sigma } _ { 1 } ) }$ .

The final equation can be obtained by simply plugging in Eq. 11 in Eq. 10.

# .11 Proof of Theorem 3

Proof. Note that the proof of Theorem 2 is modular. The additional leakage introduced by NER errors is already explicitly captured in the prompts constructed with the modified leakage function. Consequently, the remainder of the proof proceeds in exactly the same way. Our security argument remains unchanged, as it relies on a hybrid argument over prompts that differ in only a single token. So our starting point is two prompts which differ in a single token that falls in the $( 1 - \lambda ) \%$ tokens that were not replaced. □