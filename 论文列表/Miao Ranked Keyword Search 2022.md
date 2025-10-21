# Ranked Keyword Search Over Encrypted Cloud Data Through Machine Learning Method

Yinbin Miao $^{\text{©}}$ , Member, IEEE, Wei Zheng $^{\text{©}}$ , Xiaohua Jia $^{\text{©}}$ , Fellow, IEEE, Xineng Liu $^{\text{©}}$ , Member, IEEE, Kim-Kwang Raymond Choo $^{\text{©}}$ , Senior Member, IEEE, and Robert H. Deng $^{\text{©}}$ , Fellow, IEEE

Abstract—Ranked keyword search over encrypted data has been extensively studied in cloud computing as it enables data users to find the most relevant results quickly. However, existing ranked multi-keyword search solutions cannot achieve efficient ciphertext search and dynamic updates with forward security simultaneously. To solve the above problems, we first present a basic Machine Learning-based Ranked Keyword Search (ML-RKS) scheme in the static setting by using the k-means clustering algorithm and a balanced binary tree. ML-RKS reduces the search complexity without sacrificing the search accuracy, but is still vulnerable to forward security threats when applied in the dynamic setting. Then, we propose an Enhanced ML-RKS (called ML-RKS+) scheme by introducing a permutation matrix. ML-RKS+ prevents cloud servers from making search queries over newly added files via previous tokens, thereby achieving forward security. The security analysis proves that our schemes protect the privacy of indexes, query tokens and keywords. Empirical experiments using the real-world dataset demonstrate that our schemes are efficient and feasible in practical applications.

Index Terms—Ranked keyword search, k-means clustering algorithm, balanced binary tree, permutation matrix, forward security

# 1 INTRODUCTION

With the advent of cloud computing [1], more and more individuals and organizations outsource their data to cloud servers to reduce local storage and computation burden. For security concerns, the secure search [2], [3] over encrypted data has attracted increasing attention from both academic and industrial fields. There are two issues associated with the existing keyword-based search over encrypted data.

- Yinbin Miao and Wei Zheng are with the School of Cyber Engineering, Xidian University, Xi'an 710071, China, and also with the City University of Hong Kong, Hong Kong 999077, China. E-mail: ybmiao@xidian.edu.cn, zhengwei 1998@stu.xidian.edu.cn.  
Xiaohua Jia is with the Department of Computer Science, City University of Hong Kong, Hong Kong 999077, China. E-mail: csjia@cityu.edu.hk.  
- Ximeng Liu is with the Key Laboratory of Information Security of Network Systems, College of Mathematics and Computer Science, Fuzhou University, Fuzhou 350108, China. E-mail: snbnix@gmail.com.  
- Kim-Kwang Raymond Choo is with the Department of Information Systems and Cyber Security, The University of Texas at San Antonio, San Antonio, TX 78249 USA. E-mail: raymond.choo@fulbrightmail.org.  
- Robert H. Deng is with the School of Information Systems, Singapore Management University, Singapore 178902. E-mail: robertdeng@smu.edu.sg.

Manuscript received 7 June 2020; revised 9 October 2021; accepted 30 December 2021. Date of publication 4 January 2022; date of current version 6 February 2023.

This work was supported in part by the National Natural Science Foundation of China under Grants 62072361 and 61802243, in part by the Fundamental Research Funds for the Central Universities under Grant JB211505, in part by the Guangxi Key Laboratory of Cryptography and Information Security under Grant GCIS201917, in part by the Guangxi Key Laboratory of Trusted Software under Grant KX202028, and in part by the Henan Key Laboratory of Network Cryptography Technology & State Key Laboratory of Mathematical Engineering and Advanced Computing under Grant LNCT2020-A06. The work of Kim-Kwang Raymond Choo was supported by the Cloud Technology Endowed Professorship.

(Corresponding author: Yinbin Miao.)

Recommended for acceptance by B. Carminati.

Digital Object Identifier no. 10.1109/TSC.2021.3140098

The first issue is the ranked keyword search [4], [5], [6]. Existing ranked keyword search schemes can eliminate the waste of bandwidth and computation resources by returning the most relevant results rather than the entire matched results, but incur high search complexities. The key factor affecting the search complexity is the index structure used in the ranked keyword search. Inverted index [4], [7] and tree-based index [8], [9] are two commonly used index structures in existing ranked keyword search schemes. The inverted index stores a list of mappings from keywords to their corresponding set of files that contain this keyword, but achieves linear search time when ranking the results, which grows with the number of stored files. The tree-based index achieves sub-linear search time without traversing the entire files. When supporting multi-keyword searches, the inverted index and tree-based index incur higher search costs. The inverted index needs to search each keyword and intersects all search results [10], and the tree-based index needs to traverse leaf nodes containing one or more queried keywords [9]. The search complexities of the above index structures are  $O(mn)$ ,  $O(zm\log n)$ , respectively, where  $m$  is the number of keywords,  $n$  is the number of files,  $z$  is the number of files containing one or more queried keywords. When  $z$  is close to  $n$ , the tree-based index has the search complexity  $O(mz\log n) \approx O(mn\log n)$ , which causes service delay in real-time applications.

Another issue with the keyword-based encrypted data search is the forward security. The data owner often updates his/her files so that data users can enjoy real-time data sharing services. However, existing dynamic ranked keyword search schemes using the above two index structures also incur high update overhead when conducting dynamic operations such as file modification, file deletion and file addition. Strictly speaking, the inverted index is not

well-suited to handle dynamic updates, and is very complex to implement [11]. The tree-based index needs to update lots of intermediate nodes when deployed in the large-scale dataset. In addition, most existing dynamic ranked keyword search schemes are still vulnerable to potential forward security threats such as file injection attack [12].

To solve the above problems, in this paper we first present a basic Machine Learning-based Ranked Keyword Search (called ML-RKS) by using the k-means clustering algorithm [13] and balanced binary tree in the static setting, which aims to achieve efficient search over encrypted data without sacrificing the search accuracy. Then, we demonstrate an Enhanced ML-RKS (called ML-RKS+) to achieve efficient update and forward security in the dynamic setting by introducing a permutation matrix. The main contributions of our work are summarized as follows:

- We propose two efficient schemes for ranked multi-keyword search over encrypted data by using the k-means clustering technique. Our basic or enhanced scheme can return top- $k$  most relevant results from all clusters rather than a selected cluster without sacrificing the search accuracy. The file clustering process also incurs less file update overhead in the enhanced scheme.  
- We propose a permutation matrix-based method for dynamic update of outsourced files. Our enhanced scheme can achieve forward security, preventing adversaries or cloud servers from using previous query tokens to search newly added files.  
- We theoretically analyze the security and performance of our proposed schemes, and further conduct extensive experiments using the real dataset to evaluate the efficiency and feasibility.

The rest of this paper is organized as follows: Section 2 reviews the latest work regarding ranked keyword search. The system model, problem definition and threat model are presented in Section 3. The file clustering process, the construction of balanced binary tree and concrete construction of ML-RKS are illustrated in Section 4. Section 5 shows the definition of forward security and construction of ML-RKS+. Section 6 and Section 7 demonstrate the security analysis and performance analysis, respectively. Section 8 concludes this paper.

# 2 RELATED WORK

Since the first ranked keyword search scheme [4] supporting a single keyword was proposed, expressive ranked keyword search has been widely studied, including multi-keyword search, fuzzy keyword search, semantic search and phrase search. Cao et al. proposed the first ranked multi-keyword search scheme [5] to avoid returning many irrelevant search results, but this solution only supports exact keyword search. To tolerate keyword spelling errors in search queries, ranked fuzzy multi-keyword search schemes [8], [14], [15] based on locality-sensitive hashing technique, gram-based keyword transformation method or wildcard were constructed. While these schemes ignore the semantic representation information of data users' queries, which motivates the study of ranked semantic keyword search [8], [16], [17] and ranked phrase search [18]. The ranked keyword search

also focuses on other functionalities such as result verification [19], [20] and multi-owner setting [7].

However, the above-ranked keyword search schemes still incur high computation or storage burden on resource-limited entities due to inefficient index structures. For example, Cao et al. used the inverted index and TF-IDF (Term Frequency-Inverse Document Frequency) to construct the index structure, but this scheme just achieves linear search time [5]. Then, Fu et al. employed the balanced binary tree-based index structure [8], [9] to achieve sublinear search time. Besides, Li et al. utilized the ciphertext-policy attribute-based encryption [21] and blind storage [22] to construct an efficient index structure [23]. However, the search complexities of the above schemes depend on the number of stored files. To improve the search efficiency, Chen et al. [24] proposed a hierarchical clustering method based on the minimum relevance threshold, but this scheme will sacrifice the search accuracy with searching one cluster. One of the key factors affecting the search efficiency is the number of elements in matrices or spitting vectors (or the number of keywords in the dictionary) in the secure  $k$ -NN ( $k$ -Nearest Neighbor) computation. To solve this problem, Zhao et al. [25] generated the matrices and spitting vectors by using the Dual Embedding Space Model rather than the Vector Space Model (VSM).

Most existing ranked keyword search schemes in the static settings are still vulnerable to forward security threats [12]. The scheme [23] supports dynamic updates and protects the access pattern, but it does not achieve forward security. To achieve dynamic update with forward security, many forward secure search schemes [26], [27], [28], [29] have been proposed. Bost et al. [26] utilized the simple cryptographic tools such as pseudo-random functions and trapdoor permutations to guarantee the forward privacy, and further used constrained puncturable primitives [27] to achieve the same goal, but these two schemes have poor I/O performance due to relatively inefficient public key cryptographic primitive. Thus, Song et al. [28] leveraged symmetric cryptographic primitives to achieve forward privacy. However, the above schemes cannot guarantee backward privacy which means that a query token does not leak the file identities deleted later. Then, Sun et al. proposed the first practical and non-interactive backward-secure searchable symmetric encryption scheme [29] by using the puncturable pseudorandom function. To achieve ranked keyword search and forward security simultaneously, Najafi et al. [30] encrypted the index and query vectors by using a generalized permutation matrix, but still achieves linear search time. Compared with existing ranked keyword search schemes, our proposed schemes have the following features in Table 1. There are two dominant index structures such as inverted index and binary tree index. The search complexity of inverted index structure supporting multi-keyword search is  $O(nm)$ , and that of a binary tree index structure in existing ranked multi-keyword search solutions is  $O(zm\log n)$ . However, the search complexity of binary tree index structure in our proposed schemes is  $O(mz\log L_y)$ , where  $n \gg L_y$ . Thus, the search performance of our schemes outperforms that of existing solutions.

# 3 PROBLEM FORMULATION

In this section, we show the system model, problem definition and threat model, respectively.

TABLE 1 A Comparative Summary Between Our Schemes and Previous Schemes  

<table><tr><td>Schemes</td><td>Search type</td><td>Index structure</td><td>Search complexity</td><td>Supporting setting</td><td>Forward security</td></tr><tr><td>[4]</td><td>Single keyword</td><td>inverted index</td><td>O(n)</td><td>Static</td><td>X</td></tr><tr><td>[5]</td><td>Multi-keyword</td><td>—</td><td>O(nm)</td><td>Static</td><td>X</td></tr><tr><td>[14]</td><td>Fuzzy search</td><td>Bloom filter</td><td>O(nm)</td><td>Static</td><td>X</td></tr><tr><td>[8]</td><td>Synonym search</td><td>Binary tree</td><td>O(mzlog n)</td><td>Static</td><td>X</td></tr><tr><td>[18]</td><td>Phrase search</td><td>Inverted index</td><td>O(nm)</td><td>Dynamic</td><td>X</td></tr><tr><td>[9]</td><td>Multi-keyword</td><td>Binary tree</td><td>O(mzlog n)</td><td>Dynamic</td><td>X</td></tr><tr><td>[23]</td><td>Multi-keyword</td><td>Inverted index</td><td>O(nm)</td><td>Static</td><td>X</td></tr><tr><td>[30]</td><td>Multi-keyword</td><td>—</td><td>O(nm)</td><td>Dynamic</td><td>✓</td></tr><tr><td>ML-RKS</td><td>Multi-keyword</td><td>Binary tree</td><td>O(mzlog Ly)</td><td>Static</td><td>X</td></tr><tr><td>ML-RKS+</td><td>Multi-keyword</td><td>Binary tree</td><td>O(mzlog Ly)</td><td>Dynamic</td><td>✓</td></tr></table>

Notes.  $n$  is the number of files;  $m$  is the number of keywords;  $z$  is the number of leaf nodes containing one or more keywords in the search query,  $z \leq n$ ;  $L_{y}$  is the number of files in the  $y$ th cluster,  $p$  is the number of file clusters.

# 3.1 System Model

In this paper, we consider the cloud data sharing scenario. As depicted in Fig. 1, the system model of our schemes consists of three entities, namely Data Owner (DO), Cloud Server (CS) and Data Users (DUs). Specifically, the role of each entity is shown as follows:

- Data owner. DO is responsible for generating the secret key and managing DUs' access permissions. DO also builds balanced binary tree-based indexes and encrypts files. In the dynamic setting, DO is allowed to perform dynamic updates.  
- Data users. DUs make search queries by specifying weight values for queried keywords.  
- Cloud server. CS executes search operations and returns top- $k$  query results.

Before outsourcing the file set to CS, DO first generates the secret key and builds file vectors according to the keyword set and corresponding TF-IDF values, then divides them into multiple file clusters by using the  $k$ -means clustering algorithm. To facilitate an efficient search over encrypted data, DO builds the balanced binary tree-based index for each cluster. Finally, DO uploads the encrypted files and encrypted indexes to CS (Step ①). When a certain DU makes a search query, he/she first interacts with DO to obtain the secret key (Step ②), then submits the encrypted query token to CS (Step ③). CS computes the scores of encrypted indexes and encrypted query token before returning top- $k$  encrypted results to DU (Step ④).

# 3.2 Problem Definition

We use the Vector Space Model (VSM) along with TF-IDF rule for ranked multi-keyword search. Given a set of  $n$  files  $\mathcal{F} =$

Fig. 1. System model of our schemes.  
![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/1fcf8300fb08de6368af2d42a638858855eef936384a1c336cc5790ec3882d31.jpg)  
Authorized licensed use limited to: East China Normal University. Downloaded on October 13,2025 at 03:06:30 UTC from IEEE Xplore. Restrictions apply.

$\{f_1,\dots ,f_n\}$  and a set of  $m$  keywords  $\mathcal{W} = \{w_{1},\ldots ,w_{m}\}$ , TF is the frequency of a keyword  $w_{j}$  in a file  $f_{i}$  and can be calculated by  $TF_{i,j} = \frac{1 + \ln m_{i,j}}{|f_i|}$ , where  $m_{i,j}$  is the number of keyword  $w_{j}$  in the file  $d_{i}$ , and  $|f_{i}|$  is the size of file  $f_{i}$ . IDF is the inverse document frequency and is calculated by  $IDF_{j} = \ln (1 + \frac{n}{n_{j}})$ , where  $n_j$  is the number of files containing the keyword  $w_{j}$ . In VSM, each file  $f_{i}$  is associated with a file vector  $\mathbf{d}_i = (\nu_{i,1},\dots,\nu_{i,m})$ , where each element  $\nu_{i,j}$  is a normalized TF-IDF value for each keyword  $w_{j}$  and is calculated by  $TF_{i,j}\cdot IDF_{j}$ . A search query consists of a set of queried keywords. To allow users to flexibly express the weight of queried keywords, a query is represented by a vector  $\mathbf{q} = (\omega_1,\dots,\omega_m)$ , where each element  $\omega_{j}$  is the weight of queried keyword  $w_{j}$ .

The task of ranked multi-keyword search is to find the top-k most relevant files that match the query vector  $\mathbf{q}$ . For a file  $f_{i}$  and query vector  $\mathbf{q}$ , we can calculate the relevance-score  $S(\mathbf{d}_i, \mathbf{q})$  by Eq. (1). As we mentioned in the system model, all file vectors are encrypted and stored in CS, and a query vector is also encrypted as a query token and sent to CS. The task of CS is to find the top- $k$  files that produce the highest relevance scores over the encrypted data according to Eq. (1)

$$
\begin{array}{l} \mathcal {S} (\mathbf {d} _ {i}, \mathbf {q}) = \mathbf {d} _ {i} \cdot \mathbf {q} = \sum_ {w _ {j} \in q} v _ {i, j} \cdot \omega_ {j} \\ = \sum_ {w _ {j} \in q} T F _ {i, j} \cdot I D F _ {j} \cdot \omega_ {j}. \tag {1} \\ \end{array}
$$

We use the secure  $k$ -NN computation [31] to compute the relevance-score between encrypted file vector and encrypted query vector. Although this encryption mechanism doubles the ciphertext space and cannot provide stronger security, it is still efficient and feasible in terms of computation costs and supporting ranked multi-keyword search respectively when compared with cryptographic primitives [32]. Thus, this mechanism is a tradeoff between storage space and efficiency.

# 3.3 Threat Model

Similar to most ranked keyword search schemes [9], [30], [33], DO and DU are fully trusted. CS is honest-but-curious, which honestly executes the search operations but may be curious to deduce some sensitive information about files and queries. Consistent with existing solutions [34], [35], [36], the

access pattern and search pattern are beyond the scope of our discussion. For protecting the access pattern, readers can refer to existing solutions [37], [38] or other techniques such as Oblivious Random Access Memory (ORAM) [39] and Distributed Point Function (DPF) [40]. In this paper we just consider two threat models according to CS's available information, which are two basic security requirements in the generic construction of ranked keyword search.

- Known Ciphertext Model. In this model, CS has only access to encrypted balanced binary tree-based indexes  $\{\widehat{\mathcal{I}}_{\mathbf{c}_y}\}$ , encrypted files  $\{f_i^*\}$  outsourced by DO, and the encrypted query token  $\widehat{\mathbf{q}}$  submitted by each DU. CS cannot obtain the plaintext information of indexes, files and search queries.  
- Known Background Model. In comparison to the above model, CS has much more available information in this stronger model, such as dataset-related statistical information and correlation relationship of given search queries. For example, CS can deduce a certain queried keyword by combining known query tokens with file/keyword frequency information.

# 4 BASIC MACHINE LEARNING-BASED RANKED KEYWORD SEARCH (ML-RKS)

This section presents the design of our basic scheme (ML-RKS) in detail. We first introduce the construction of a balanced binary tree, then give the concrete construction of ML-RKS.

# 4.1 Building Balanced Binary Tree

To greatly reduce the search complexity without sacrificing the search accuracy, the main idea of our basic scheme is to utilize the k-means clustering algorithm [24], [41] to divide the entire file vectors into  $p$  clusters. Given a set of file vectors  $\{\mathbf{d}_1,\dots ,\mathbf{d}_n\}$ , DO first chooses  $p$  initial cluster vectors  $\{\mathbf{c}_1,\ldots ,\mathbf{c}_p\}$ , then adds each file vector  $\mathbf{d}_i$  to the  $y$ th cluster such that the relevance-score  $S(\mathbf{d}_i,\mathbf{c}_y)$  is the highest, finally obtains  $p$  clusters until all file vectors are added. To achieve sub-linear search time, we use a balanced binary tree [9] to build the index structure. Let  $L_{y}$  be the number of file vectors  $\{\mathbf{d}_1,\dots ,\mathbf{d}_{L_y}\}$  in the  $y$ th cluster,  $\mathbf{d}_i[j]$  be  $j$ th TF-IDF value  $v_{i,j}$  of keyword  $w_{j}$  in the file vector  $\mathbf{d}_i$ , we construct the  $y$ th balanced binary tree in Algorithm 1. The process consists of two steps as follows:

1) The balanced binary tree generates the leaf nodes according to file vectors  $\{\mathbf{d}_1,\dots ,\mathbf{d}_{L_y}\}$ .  
2) The internal node and root node vectors are generated in a bottom-up manner. For each internal node vector  $\mathbf{d}_x$ , its value of each element is determined by its child node vector  $\mathbf{d}_l$  and right child vector  $\mathbf{d}_r$ , namely  $\mathbf{d}_x[j] = \max \{\mathbf{d}_l[j], \mathbf{d}_r[j]\}$ . The root node vector is generated recursively.

Note that each cluster vector is replaced with the root node vector of corresponding balanced binary tree. Fig. 2 demonstrates how to search the selected balanced binary tree according to a query vector  $\mathbf{q} = (0.1, 0.5, 02)$ . Given the keyword set  $\{w_1, w_2, w_3\}$  and a set of file vectors  $\{\mathbf{d}_1, \ldots, \mathbf{d}_6\}$ , we search this balanced binary tree with root

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/f82c7f1d63131f0742d8ef6f2319562d43404ab1ed9b00f9d4a4e6908b490e76.jpg)  
Fig. 2. An example for searching the balanced binary tree.

node vector  $\mathbf{n}_{ro} = (0.6, 0.7, 0.7)$  to find top-2 results. The procedure is shown as follows:

1) According to Eq. (1), we have  $S(\mathbf{n}_{1,0},\mathbf{q}) > S(\mathbf{n}_{1,1},\mathbf{q})$ . Thus, we search the subtree with root node vector  $\mathbf{n}_{1,0}$ , then continue to search the subtree with root note vector  $\mathbf{n}_{2,0}$  due to  $S(\mathbf{n}_{2,0},\mathbf{q}) > S(\mathbf{n}_{2,1},\mathbf{q})$ .  
2) We compute the scores  $S(\mathbf{d}_1, \mathbf{q}) = 0.46$  and  $S(\mathbf{d}_2, \mathbf{q}) = 0.39$ . Due to  $S(\mathbf{n}_{2,1}, \mathbf{q}) = 0.22 < 0.39$ , we do not need to calculate the scores between  $\mathbf{d}_3, \mathbf{d}_4$  and  $\mathbf{q}$ .  
3) Due to  $S(\mathbf{n}_{1,1}, \mathbf{q}) = 0.40 > 0.39$ , we need to compute  $S(\mathbf{d}_5, \mathbf{q}) = 0.32$  and  $S(\mathbf{d}_6, \mathbf{q}) = 0.40$ . The top-2 results  $\mathbf{d}_1, \mathbf{d}_6$  will be returned.

# Algorithm 1. Building Plaintext Balanced Binary Tree-Based Index for the  $y$ th Cluster

Input: file set  $\{f_1,\dots ,f_{L_y}\}$  in cluster cy Output: Plaintext balanced binary tree-based index  $\mathcal{I}_{\mathbf{c}_y}$    
1: Obtain file vectors  $\{\mathbf{d}_1,\dots ,\mathbf{d}_{L_y}\}$  .   
2: foreach di do   
3: Store di in vector array  $D$  .   
4: Node node=new Node();   
5: node.value  $= D[i]$  .   
6:  $D[i] =$  node;   
7: Calculate the number of nodes at the bottom layer  ${\mathrm{Num}}=2L_{y}-2^{h-1};/\ast h$  is height of balanced binary tree \*/   
8: for  $i = 1;i\leq N u m;i + + d o$    
9: Node node=new Node(); /\* Create new node \*/   
10: for  $j = 1;\iota \leq \widetilde{m};j + + d o$    
11: node.value[j]=max(D[i].value[j],D[i+1].value[j]);   
12:  $D[i / 2] =$  node;   
13: for  $i = N u m + 1;i\leq L_{y};i + + d o$    
14: Adding the remaining nodes in array, namely  $D[i - Num / 2] = D[i]$    
15: foreach node in D do   
16: Node node=new Node(); /\* Create parent node \*/   
17: for  $j = 1;j\leq \tilde{m};j + + d o$    
18: node.value[j]=max(D[i].value[j],D[i+1].value[j]);   
19:  $D[i / 2] =$  node;   
20: Connect parent node to child node with pointer;   
21: Repeat 15-20 until there is one node in  $D$  and output the root node;   
22: Return the plaintext balanced binary tree-based index  $\mathcal{I}_{\mathbf{c}_y}$

For security concerns, we extend the splitting vector  $\mathbf{S} \in \{0,1\}^{\widetilde{m}}$  and two invertible matrices  $\mathbf{M}_1, \mathbf{M}_2 \in \mathbb{R}^{\widetilde{m} \times \widetilde{m}}$ , which will be explained in the constructions of our schemes. Next, we encrypt the plaintext balanced binary tree by using the secure  $k$ -NN computation technique. There are three kinds of nodes in each balanced binary tree, such as root node (or cluster vector)  $\mathbf{c}_y \in \mathbb{R}^{\widetilde{m}}$ , intermediate nodes  $\mathbf{d}_x \in \mathbb{R}^{\widetilde{m}}$  and leaf nodes (or file vectors)  $\mathbf{d}_i \in \mathbb{R}^{\widetilde{m}}$ . Then, we leverage the extended  $k$ -NN algorithm to encrypt  $\mathbf{d}_i, \mathbf{c}_y, \mathbf{d}_x, \mathbf{q}$  as  $\widehat{\mathbf{d}}_i, \widehat{\mathbf{c}}_y, \widehat{\mathbf{d}}_x, \widehat{\mathbf{q}}$  in Algorithm 2, thereby gaining the encrypted index  $\widehat{I}_{\mathbf{c}_y}$  for cluster  $\mathbf{c}_y$ . Finally, we have Eq. (2) according to Eq. (1)

$$
\left\{ \begin{array}{l} S (\widehat {\mathbf {d}} _ {i}, \widehat {\mathbf {q}}) = \widehat {\mathbf {d}} _ {i} \cdot \widehat {\mathbf {q}} = \mathbf {d} _ {i} \cdot \mathbf {q} = S (\mathbf {d} _ {i}, \mathbf {q}); \\ S (\widehat {\mathbf {d}} _ {x}, \widehat {\mathbf {q}}) = \widehat {\mathbf {d}} _ {x} \cdot \widehat {\mathbf {q}} = \mathbf {d} _ {x} \cdot \mathbf {q} = S (\mathbf {d} _ {x}, \mathbf {q}); \\ S (\widehat {\mathbf {c}} _ {y}, \widehat {\mathbf {q}}) = \widehat {\mathbf {c}} _ {y} \cdot \widehat {\mathbf {q}} = \mathbf {c} _ {y} \cdot \mathbf {q} = S (\mathbf {c} _ {y}, \mathbf {q}). \end{array} \right. \tag {2}
$$

Given the encrypted search query  $\widehat{\mathbf{q}}$  submitted by each DU, CS first computes the scores  $S(\widehat{\mathbf{c}}_1,\widehat{\mathbf{q}}),\ldots ,S(\widehat{\mathbf{c}}_p,\widehat{\mathbf{q}})$  by Eq. (2) and selects the cluster with highest score  $S(\widehat{\mathbf{c}}_y,\widehat{\mathbf{q}})$  then retrieves the top-  $k$  results from the balanced binary tree constructed for this selected cluster. It is worth noticing that all file vectors contained in various clusters are encrypted by the same mechanism and use the same normalization factor. Simply implementing this process can improve the search efficiency, but may reduce the search accuracy. To prevent accuracy degradation, we need to check whether the scores between top-  $k$  results and query are greater than or equal to those between unselected clusters and query, which will be discussed in the concrete constructions of our proposed schemes.

Algorithm 2. The Encryption for Different Vectors  
Input: Plaintiff file vector  $\mathbf{d}_i$  , cluster vector  $\mathbf{c}_y$  , intermediate node vector  $\mathbf{d}_x$  query vector q and secret key  $SK = \{\mathbf{S},\mathbf{M}_1,\mathbf{M}_2\}$  Output: Encrypted vectors  $\widehat{\mathbf{d}}_i,\widehat{\mathbf{c}}_y,\widehat{\mathbf{d}}_x,\widehat{\mathbf{q}}$  1: Split  $\mathbf{d}_i,\mathbf{c}_y,\mathbf{d}_x,\mathbf{q}$  as  $(\mathbf{d}_{i,1},\mathbf{d}_{i,2}),(c_{y,1},c_{y,2}),(d_{x,1},d_{x,2}),(q_1,q_2)$  . 2: Encrypt  $\widehat{\mathbf{d}}_i,\mathbf{c}_y,\mathbf{d}_x$  . 3: for  $j = 1;j\leq \tilde{m};j + = 1$  do 4: if S[j] = 0 then 5:  $\mathbf{d}_{i,1}[j] = \mathbf{d}_{i,2}[j] = \mathbf{d}_i[j]$  . 6:  $\mathbf{c}_{y,1}[j] = \mathbf{c}_{y,2}[j] = \mathbf{c}_y[j]$  . 7:  $\mathbf{d}_{x,1}[j] = \mathbf{d}_{x,2}[j] = \mathbf{d}_x[j]$  . 8: else 9:  $\mathbf{d}_{i,1}[j] + \mathbf{d}_{i,2}[j] = \mathbf{d}_i[j]$  . 10:  $\mathbf{c}_{y,1}[j] + \mathbf{c}_{y,2}[j] = \mathbf{c}_y[j]$  . 11:  $\mathbf{d}_{x,1}[j] + \mathbf{d}_{x,2}[j] = \mathbf{d}_x[j]$  . 12: Encrypt q; 13: for  $j = 1;j\leq \widetilde{m};j + = 1$  do 14: if S[j] = 0 then 15:  ${\bf q}_1[j] + {\bf q}_2[j] = {\bf q}[j]$  . 16: else 17:  ${\bf q}_1[j] = {\bf q}_2[j] = {\bf q}[j]$  . 18: Encrypt d as  $\widehat{\mathbf{d}}_i = (\mathbf{M}_1^\top \mathbf{d}_{i,1},\mathbf{M}_2^\top \mathbf{d}_{i,2})$  . 19: Encrypt c y as  $\widehat{\mathbf{c}}_{\underline{\boldsymbol{\mu}}} = (\mathbf{M}_1^\top \mathbf{c}_{\boldsymbol{\mu},\boldsymbol{\mu}},\mathbf{M}_2^\top \mathbf{c}_{\boldsymbol{\mu},\boldsymbol{\mu}})$  . 20: Encrypt d x as d  $x = (\mathbf{M}_1^\top \mathbf{d}_{x,1},\mathbf{M}_2^\top \mathbf{d}_{x,2})$  . 21: Encrypt q as q  $= (\mathbf{M}_1^{-1}\mathbf{q}_1,\mathbf{M}_2^{-1}\mathbf{q}_2)$  . 22: Return d i,  $\widehat{\mathbf{c}}_y,\widehat{\mathbf{d}}_x,\widehat{\mathbf{q}}$

# 4.2 Construction of ML-RKS

The ranked keyword search based on the secure  $k$ -NN computation is just secure in the known ciphertext model, but cannot guarantee the keyword privacy in the known background model as CS may have some background information such as the correlation relationship of two given query tokens. Specifically, CS can use the scale analysis [5] to deduce the sensitive information of keywords, thereby compromising the keyword privacy. To solve this problem, we add  $U$  dummy keywords in the secure  $k$ -NN computation. In addition, CS learns the relationship among the received query tokens so that it can determine whether two query tokens are generated from the same search query. Introducing some randomness in the query vector is an elegant way to achieve token indistinguishability. Finally, we add an extra element in each file vector and query vector to achieve forward security in  $\mathrm{ML - RKS^{+}}$ , which will be explained in detail in Section 5. Thus, the secret key  $SK = (\mathbf{M}_1,\mathbf{M}_2,\mathbf{S})$  is extended as  $\mathbf{S}\in \{0,1\}^{\widetilde{m}}$ ,  $\mathbf{M}_1,\mathbf{M}_2\in \mathbb{R}^{\widetilde{m}\times \widetilde{m}}$ , where  $\widetilde{m} = m + U + 2$ .

The concrete construction of ML-RKS, which consists of several phases such as key generation, indexes & ciphertexts generation, query token generation and ciphertext search.

Key generation. Given the security parameter  $\kappa$ , DO generates the secret key  $SK = (\mathbf{S}, \mathbf{M}_1, \mathbf{M}_2, k_e)$ , where  $k_e$  is the key of symmetric encryption algorithm such as AES or DES,  $\mathbf{S} \in \{0, 1\}^{\widetilde{m}}$ ,  $\mathbf{M}_1, \mathbf{M}_2 \in \mathbb{R}^{\widetilde{m} \times \widetilde{m}}$ .

Indexes ciphertexts generation. Let  $\mathcal{F} = \{f_1,\dots ,f_n\}$  be the files,  $\mathcal{W} = (w_{1},\ldots ,w_{m})$  be the keywords, DO generates  $\mathbf{d}_i = \{\nu_{i,1},\dots ,\nu_{i,m},\varepsilon_{i,m + 1},\dots ,\varepsilon_{i,m + U},1,1\} \in \mathbb{R}^{\widetilde{m}}$  which is different from the scheme in [5]. It is worth noticing that each file vector in ML-RKS has  $m + U + 2$  elements. The first  $m$  elements of  $\mathbf{d}_i$  are normalized TF-IDF values  $\{\nu_{i,1},\dots ,\nu_{i,m}\}$  generated by Eq. (1). The random elements  $\{\varepsilon_{i,m + 1},\dots ,\varepsilon_{i,m + U}\}$  of  $\mathbf{d}_i$  follow the normal distribution  $N(\mu ,\sigma^2)$ , where the standard deviation  $\sigma$  is a tradeoff parameter among search accuracy and security. The last two elements of  $\mathbf{d}_i$  are both set as "1" to achieve token indistinguishability and forward security. Then, DO encrypts each file  $f_{i}\in \mathcal{F}$  as  $f_{i}^{*}$  by using the symmetric encryption key  $k_{e}$  and  $\mathbf{d}_i$  as  $\widehat{\mathbf{d}}_i$  by utilizing Algorithm 2, where  $\widehat{\mathbf{d}}_i = (\mathbf{M}_1^\top \mathbf{d}_{i,1},\mathbf{M}_2^\top \mathbf{d}_{i,2})$

To improve the search efficiency, DO first divides these file vectors  $\{\mathbf{d}_1,\dots ,\mathbf{d}_n\}$  into multiple clusters  $\{\mathbf{c}_1,\mathbf{c}_2,\dots ,\mathbf{c}_p\}$  by using the  $k$  -means clustering algorithm [42]. Assume that there are  $L_{y}$  file vectors  $\{\mathbf{d}_1,\ldots ,\mathbf{d}_{L_y}\}$  in each cluster, DO builds the plaintext balanced binary tree-based index  $\mathcal{I}_{\mathbf{c}_y}$  for each cluster  $\mathbf{c}_y$  by calling Algorithm 1. To generate the encrypted balanced binary tree-based index  $\widehat{\mathcal{I}}_{\mathbf{c}_y}$  DO just encrypts each node vector in plaintext balanced binary tree-based index  $\mathcal{I}_{\mathbf{c}_y}$  by using the secret key  $SK$  . For example, each cluster vector  $\mathbf{c}_y$  is encrypted as  $\widehat{\mathbf{c}}_y = (\mathbf{M}_1^\top \mathbf{c}_{y,1},\mathbf{M}_2^\top \mathbf{c}_{y,2})$  and each intermediate node vector  $\mathbf{d}_x$  is encrypted as  $(\mathbf{M}_1^\top \mathbf{d}_{x,1},\mathbf{M}_2^\top \mathbf{d}_{x,2})$  by using Algorithm 2. Finally, DO uploads encrypted files  $\{f_i^*\}$  and encrypted balanced binary tree-based indexes  $\{\widehat{\mathcal{I}}_{\mathbf{c}_y}\}$  to CS.

Query token generation. When making the search query  $q$ , DU first specifies weight values  $\{\omega_1, \ldots, \omega_m\}$  for queried keywords, where  $\omega_j \in [0, 1]$ . If the keyword  $w_j \notin q$ , DU sets

$\omega_{j} = 0$  otherwise,  $\omega_{j}$  is set as a non-zero value. Then, DU randomly selects  $V$  out of  $U$  dummy keywords and sets corresponding weight values as 1, and the weight values of remaining dummy keywords are set as 0. Besides, DU selects two random elements  $\alpha ,\beta$  to guarantee token indistinguishability. Finally, DO generates the query vector  $\mathbf{q} = (\alpha \omega_1,\dots ,\alpha \omega_m,\alpha ,0,0,\dots ,\alpha ,\beta ,1)\in \mathbb{R}^m$  note that the number of elements satisfying  $\mathbf{q}[j] = \alpha (j\in [m + 1,m + U])$  is  $V$  After obtaining the secret key  $SK$  from DO, DU encrypts  $\mathbf{q}$  as  $\widehat{\mathbf{q}} = (\mathbf{M}_1^{-1}\mathbf{q}_1,\mathbf{M}_2^{-1}\mathbf{q}_2)$  by utilizing Algorithm 2, then sends the encrypted query token  $\widehat{\mathbf{q}}$  and parameter  $k$  to CS.

Ciphertext search. Upon receiving the encrypted query vector  $\widehat{\mathbf{q}}$  and  $k$ , CS first computes the scores between  $\{\widehat{\mathbf{c}}_y\}$  and  $\widehat{\mathbf{q}}$  by Eq. (2). Then, CS selects the cluster with highest score  $S(\widehat{\mathbf{c}}_y, \widehat{\mathbf{q}})$ , and searches the top- $k$  results from corresponding encrypted balanced binary tree by Eq. (2)

$$
\begin{array}{l} \mathcal {S} (\widehat {\mathbf {d}} _ {i}, \widehat {\mathbf {q}}) = \widehat {\mathbf {d}} _ {i} \cdot \widehat {\mathbf {q}} = \mathbf {M} _ {1} ^ {\top} \mathbf {d} _ {i, 1} \cdot \mathbf {M} _ {1} ^ {- 1} \mathbf {q} _ {1} + \mathbf {M} _ {2} ^ {\top} \mathbf {d} _ {i, 2} \cdot \mathbf {M} _ {2} ^ {- 1} \mathbf {q} _ {2} \\ = \mathbf {d} _ {i} \cdot \mathbf {q} = \alpha \left(\sum_ {j = 1} ^ {m} v _ {i, j} \omega_ {j} + \sum_ {j = 1 + m} ^ {m + U} \varepsilon_ {i, j}\right) + \beta + 1. \\ \end{array}
$$

To return the exact top- $k$  results, CS needs to check the following two cases:

- Case 1. If the score between the  $k$ th result and query is greater than or equal to those between other clusters and query, the top- $k$  results are directly returned to DU.  
- Case 2. If some scores between top- $k$  results and query are less than those between other clusters and query, CS needs to compute scores between files in other clusters and query. CS updates the top- $k$  results and stops until the score between the  $k$ th result and query is not less than those between other clusters or intermediate nodes and query.

Remark 1. With the k-means clustering algorithm, the minimum search complexity of ML-RKS can be reduced to  $O(mz\log L_y)$  in Case 1. In Case 2, the maximum search complexity is about  $O(mz\log L_y)$ , which is still smaller than  $O(mn\log n)$  in previous balanced binary tree-based schemes due to  $zp \ll n$ . ML-RKS also enables DUs to specify weight values for queried keywords without computing corresponding IDF values. These two features in ML-RKS reduce the computation costs of ciphertext search and query token generation. In addition, ML-RKS adds some random elements when encrypting file vectors and query vectors, thereby hiding the plaintext relevance scores. Thus, CS cannot deduce the plaintext relevance scores by computing  $S(\widehat{\mathbf{d}}_i, \widehat{\mathbf{q}})$ , and even cannot determine whether two file vectors are the same if  $S(\widehat{\mathbf{d}}_i, \widehat{\mathbf{q}}) = S(\widehat{\mathbf{d}}_j, \widehat{\mathbf{q}})$ . However, ML-RKS is just suitable for the static setting. Simply deploying ML-RKS in the dynamic setting will lead to two challenging issues such as time-consuming dynamic updates and forward-security threat. First, existing tree-based index structures need to update many intermediate nodes when dealing with file modification or file deletion operation, and even need to rebuild the tree structure to conduct file addition operation. Second, ML-RKS with dynamic updates may be vulnerable to potential forward security threats

such as injection attacks [12]. Thus,  $\mathrm{ML - RKS^{+}}$  should provide efficient dynamic updates with forward security.

# 5 ENHANCED MACHINE LEARNING-BASED RANKED KEYWORD SEARCH (ML-RKS+)

This section first gives the definition of forward security and the solution to forward security threats, then demonstrates the construction of ML-RKS+.

# 5.1 Forward Security

In the dynamic setting, assume that CS has performed search operation for the token  $\widehat{\mathbf{q}}$  and returned the result set  $\mathcal{R}$ . Later, DO adds an encrypted file vector  $\widehat{\mathbf{d}}_i$ . If CS gains the result set  $\mathcal{R}'$  by using the previous token  $\widehat{\mathbf{q}}$ , note that  $\mathcal{R}$  and  $\mathcal{R}'$  have only one different result. Then, CS learns that the newly added file vector satisfies  $\widehat{\mathbf{q}}$ , which will compromise the forward security. Thus, it requires that CS cannot know whether newly added file vectors satisfy previous tokens. To avoid this privacy leakage, the previous token cannot be used to make search queries after file update operations. Otherwise, CS may launch an adaptive attack by inserting some newly-added files [12], aiming to learn a very high fraction of information about keyword set contained in previous tokens.

To achieve forward security in our enhanced scheme, ML-RKS $^{+}$  should thwart this type of attack by preventing adversaries or CS from determining the keywords queried before injecting malicious files. Some typical techniques such as trapdoor permutations [43], puncturable encryption [44] can be used to achieve this goal, but still cannot support the ranked keyword search. Although the permutation matrix has been used in [30], [45], [46], these solutions still have the linear search complexity due to the use of a forward index. In ML-RKS $^{+}$ , we generate a permutation matrix based on the version number and then allow CS to update each encrypted file vector. If the adversary (e.g., CS) successfully makes search queries, he/she should generate valid query tokens according to this permutation matrix. It is worth noticing that the permutation matrix is just shared among DO and authorized DUs, thereby preventing adversaries or CS to search newly added files using previous query tokens.

# 5.2 Construction of ML-RKS+

We give the construction of ML-RKS $^+$  by presenting the modified content in these phases of ML-RKS and adding the file update phase.

Key generation. In addition to generating the secret key  $SK = (\mathbf{S}, \mathbf{M}_1, \mathbf{M}_2, k_e)$ , DO also chooses a hash function  $\mathcal{H} : \{0, 1\}^* \to \mathcal{N}$  and a permutation matrix  $\mathbf{P} \in \mathbb{R}^{m \times m}$ , where  $\mathcal{N}$  is the natural number set. Note that  $\mathbf{P}$  and any power of it just have one element "1" in every row and every column. DO sets the secret key as  $SK^* = (SK, \mathcal{H}, \mathbf{P})$ .

Indexes ciphertexts generation. After generating the encrypted files  $\{f_i^*\}$  and encrypted indexes  $\{\widehat{\mathcal{I}}_{\mathbf{c}_y}\}$  in the same way as ML-RKS, DO first computes  $\mathbf{P}^{\delta_{ver}}$ , where  $\delta_{ver} = \mathcal{H}(\det(\mathbf{M}_1)|\det(\mathbf{M}_2)|ver)$  and the initial value of version number  $ver$  is set as '0'. Then, DO replaces the element "1" in the last row of  $\mathbf{P}^{\delta_{ver}}$  with  $\theta = \frac{\delta_{ver} + 1}{\delta_{ver}} + \frac{\delta_{ver}}{\delta_{ver} + 1}$ , thereby converting  $\mathbf{P}^{\delta_{ver}}$  to  $\mathbf{P}_{ver}$ . Finally, DO encrypts  $\mathbf{P}_{ver}$  as  $\widehat{\mathbf{P}}_{ver} =$

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/a36c1fb24cd44737174aa7a79c2efd5fc45555bcfe70cbe97a400bb2d4abee53.jpg)  
Fig. 3. Example for file update.

$(\mathbf{M}_1^{-1}\mathbf{P}_{ver}\mathbf{M}_2^\top ,\mathbf{M}_2^{-1}\mathbf{P}_{ver}\mathbf{M}_1^\top)$ . DO multiplies each node vector in  $\hat{\mathcal{I}}_{\mathbf{c}_y}$  by  $\hat{\mathbf{P}}_{ver}$ , thereby updating  $\hat{\mathcal{I}}_{\mathbf{c}_y}$  as  $\{\hat{\mathcal{I}}_{\mathbf{c}_y}^t\}$ . For example, the encrypted root node vector  $\hat{\mathbf{c}}_y$  is updated as  $\hat{\mathbf{c}}_y\cdot \hat{\mathbf{P}}_{ver}$ .

Query token generation. Before making the search query  $q$ , DU obtains the secret key  $SK^{*} = (SK, \mathcal{H}, \mathbf{P})$  by interacting with DO. The generation and splitting processes of query vector  $\mathbf{q} = (\mathbf{q}_1, \mathbf{q}_2)$  in ML-RKS+ are similar to those in ML-RKS. To generate the query token, DU also needs to compute  $\mathbf{P}^{\delta_{ver}} = \mathbf{P}^{\mathcal{H}(\text{det}(\mathbf{M}_1)|\text{det}(\mathbf{M}_2)|ver)}$ . The encrypted query token is defined as  $\hat{\mathbf{q}}' = (\mathbf{M}_2^{-1}\mathbf{P}^{\delta_{ver}}\mathbf{q}_1, \mathbf{M}_1^{-1}\mathbf{P}^{\delta_{ver}}\mathbf{q}_2)$ . Finally, DU sends  $\hat{\mathbf{q}}'$  as well as parameter  $k$  to CS

$$
\begin{array}{l} \mathcal {S} \left(\widehat {\mathbf {c}} _ {y} \cdot \widehat {\mathbf {P}} _ {v e r}, \widehat {\mathbf {q}} ^ {\prime}\right) = \widehat {\mathbf {c}} _ {y} \cdot \widehat {\mathbf {P}} _ {v e r} \cdot \widehat {\mathbf {q}} ^ {\prime} \\ = \mathbf {M} _ {1} ^ {\top} \mathbf {c} _ {y, 1} \mathbf {M} _ {1} ^ {- 1} \mathbf {P} _ {v e r} \mathbf {M} _ {2} ^ {\top} \mathbf {M} _ {2} ^ {- 1} \mathbf {P} ^ {\delta_ {v e r}} \mathbf {q} _ {1} + \\ \mathbf {M} _ {2} ^ {\top} \mathbf {c} _ {y, 2} \mathbf {M} _ {2} ^ {- 1} \mathbf {P} _ {v e r} \mathbf {M} _ {1} ^ {\top} \mathbf {M} _ {1} ^ {- 1} \mathbf {P} _ {v e r} ^ {\delta_ {v e r}} \mathbf {q} _ {2} \\ = \mathbf {c} _ {y} \mathbf {P} _ {v e r} \mathbf {P} ^ {\delta_ {v e r}} \mathbf {q} \tag {3} \\ \end{array}
$$

Ciphertext search. According to Eq. (2), CS first computes the scores between query token  $\widehat{\mathbf{q}}'$  and cluster vectors  $\{\widehat{\mathbf{c}}_y \cdot \widehat{\mathbf{P}}_{ver}\}$  by Eq. (3) and chooses the cluster with highest score. Then, CS computes the scores between  $\widehat{\mathbf{q}}'$  and encrypted file vectors  $\widehat{\mathbf{d}}_i'$  by Eq. (4). Finally, CS sends the top- $k$  query results to DU. There are also two cases in this phase, which are same as those in ML-RKS

$$
\begin{array}{l} S \left(\widehat {\mathbf {d}} _ {i} ^ {\prime}, \widehat {\mathbf {q}} ^ {\prime}\right) = \widehat {\mathbf {d}} _ {i} ^ {\prime} \cdot \widehat {\mathbf {q}} ^ {\prime} = \mathbf {d} _ {i} \mathbf {P} _ {v e r} \mathbf {P} ^ {\delta_ {v e r}} \mathbf {q} \\ = \alpha \sum_ {j = 1} ^ {m} v _ {i, j} + \alpha \sum_ {j = m + 1} ^ {m + U} \varepsilon_ {i, j} + \beta + \theta . \tag {4} \\ \end{array}
$$

File update. When DO executes the update operations such as file modification, file deletion and file addition, DO first updates the version number as  $ver' = ver + 1$  and computes  $\mathbf{P}^{\delta_{ver'}}$ , where  $\delta_{ver'} = \mathcal{H}(\det(\mathbf{M}_1)|\det(\mathbf{M}_2)|ver')$ . Then, DO generates  $\mathbf{P}_{\delta_{ver'}}$  by replacing the element "1" in the last row with  $\theta' = \frac{\delta_{ver'} + 1}{\delta_{ver'}} + \frac{\delta_{ver'}}{\delta_{ver'} + 1}$ . Finally, DO encrypts  $\mathbf{P}^{\delta_{ver'}}$  as  $\hat{\mathbf{P}}_{\delta_{ver'}}$  and updates the encrypted file vector as  $\hat{\mathbf{d}}_i \cdot \hat{\mathbf{P}}_{\delta_{ver'}}$ . Next, we list an example to show how to deal with the above update operations in Fig. 3, note that the cluster  $\mathbf{c}_1$  contains four file vectors  $\{\mathbf{d}_1, \mathbf{d}_2, \mathbf{d}_3, \mathbf{d}_4\}$  and the initial value of version number  $ver$  is set as 0. There are three different update operations in the following:

- File modification. If DO wants to modify the file vector  $\mathbf{d}_1$  as  $\mathbf{d}_1'$ , he/she first updates node vectors  $\mathbf{n}_1, \mathbf{c}_1$ . Then, DO generates  $\widehat{\mathbf{P}}_1$  ( $ver' = 0 + 1 = 1$ ). Finally, DO encrypts all node vectors in the balanced binary tree by multiplying  $\widehat{\mathbf{P}}_1$ . For example, the modified file vector  $\mathbf{d}_1'$  is encrypted as  $\widehat{\mathbf{d}}_1' \cdot \widehat{\mathbf{P}}_1$ .

- File deletion. If DO wants to delete the file vector  $\mathbf{d}_2$ , he/she first sets  $\mathbf{d}_2 = \{0, \dots, 0\}$  and updates node vectors  $\mathbf{n}_1, \mathbf{c}_1$ . Then, DO generates  $\widehat{\mathbf{P}}_2$  ( $ver' = 1 + 1 = 2$ ). Finally, DO updates all encrypted node vectors by multiplying  $\widehat{\mathbf{P}}_2$ .

- File addition. If DO wants to add the file vector  $\mathbf{d}_5$ , DO puts file vectors  $\mathbf{d}_4, \mathbf{d}_5$  in the next level of balanced binary tree and updates node vectors  $\mathbf{c}_1, \mathbf{n}_2, \mathbf{n}_3$ , then generates  $\widehat{\mathbf{P}}_3$  ( $ver' = 2 + 1 = 3$ ). Finally, DO updates all node vectors by multiplying  $\widehat{\mathbf{P}}_3$ .

Remark 2. In addition to having the advantages of ML-RKS, our proposed ML-RKS+ also achieves efficient update operations and forward security in the dynamic setting. One difference is that ML-RKS uses the  $(m + U + 1)$ th element to guarantee the token indistinguishability. While ML-RKS+ also uses the  $(m + U + 1)$ th and  $(m + U + 2)$ th elements to guarantee that indexes and tokens are in the same version number. With the k-means clustering algorithm, ML-RKS+ only needs to update the selected cluster rather than all clusters, which incurs less update overhead. Apart from adding randomness in encrypted file vectors and query vectors, ML-RKS+ also adds a random element  $\theta$  associated with the version number, so that CS cannot use previous tokens to retrieve newly added file vectors. Due to the use of balanced binary tree-based index structure, the theoretical update overhead of file modification or file deletion is about  $(\log L_y + 1)\mathbb{E}_{\mathbf{v}} + (2n - 1)\mathbb{M}_{\mathbf{v}}$ , and that of file addition is about  $(\log L_y + 2)\mathbb{E}_{\mathbf{v}} + (2n + 1)\mathbb{M}_{\mathbf{v}}$ . It is noted that  $\mathbb{E}_{\mathbf{v}}$  is the encryption of  $(m + U + 2)$ -dimension by calling secure  $k$ -NN algorithm, and  $\mathbb{M}_{\mathbf{v}}$  is the inner product between any two  $(m + U + 2)$ -dimension vectors. As the generation of permutation matrix  $\mathbf{P}_{ver}$  based on the updated version number prevents CS from launching file injection attacks, our ML-RKS+ achieves the forward security.

# 6 SECURITY ANALYSIS

As for the file privacy, the traditional symmetric encryption can be used to guarantee its confidentiality if DO and DUs do not leak the symmetric key  $k_{e}$ . Then, we briefly prove the security of ML-RKS or ML-RKS $^{+}$ .

Theorem 1. ML-RKS or ML-RKS+ guarantees the index and query confidentiality in both known ciphertext model and known background model if CS does not obtain the secret keys  $(\mathbf{M}_1, \mathbf{M}_2, \mathbf{S})$ .

Proof. For simplicity, we take ML-RKS as an example. CS can only obtain encrypted file vectors  $\{(\mathbf{M}_1^\top \mathbf{d}_{i,1},\mathbf{M}_2^\top \mathbf{d}_{i,2})\}$  and encrypted query token  $(\mathbf{M}_1^{-1}\mathbf{q}_1,\mathbf{M}_2^{-1}\mathbf{q}_2)$ . For the linear equations constructed from the index set  $\{\widehat{\mathbf{d}}_1,\dots ,\widehat{\mathbf{d}}_n\}$ , there exist  $2nm$  unknowns due to the randomness of splitting vector S. Due to the randomness of matrices  $\mathbf{M}_1,\mathbf{M}_2$ , there also exist  $2m^2$  unknowns. Assume that CS is given  $2nm$  equations in encrypted indexes, he/she still cannot deduce any sensitive information as there are  $2m^2 + 2nm$  unknowns in total, thereby guaranteeing the index confidentiality in the above two threat models. As for the query token, there exist  $2m$  equations. CS still cannot deduce the underlying query keywords as there are  $2m^2$  unknowns, thereby guaranteeing the query confidentiality.

Theorem 2. Our ML-RKS or ML-RKS $^+$  achieves the query token indistinguishability for the same query request.

Proof. For the submitted query token, its randomness can be guaranteed due to randomly splitting in the encrypted query token  $\hat{\mathbf{q}}$ . Given two query vectors  $\mathbf{q}', \mathbf{q}''$ , they will be split as two random values when  $\mathbf{S}[j] = 0$ , namely  $\mathbf{q}' = (\mathbf{q}_1', \mathbf{q}_2')$ ,  $\mathbf{q}'' = (\mathbf{q}_1'', \mathbf{q}_2'')$ . Assume that the probability of  $Pr[(\mathbf{q}_1'[j], \mathbf{q}_2'[j]) = (\mathbf{q}_1''[j], \mathbf{q}_2''[j])]$  is  $\gamma$ , then the probability that CS obtains the same query vector (e.g.,  $\mathbf{q}' = \mathbf{q}''$ ) is  $\gamma^\epsilon$ , where  $\epsilon$  is the number of zeros in the splitting vector  $\mathbf{S}$ . As  $(\mathbf{q}_1', \mathbf{q}_2')$ ,  $(\mathbf{q}_1'', \mathbf{q}_2'')$  are random pairs, the value  $\gamma$  is far less than  $\frac{1}{2}$ . The larger the value  $\epsilon$  is, the smaller  $\gamma^\epsilon$  is. In other words, the probability of  $\mathbf{q}' = \mathbf{q}''$  is close to zero. Thus, the probability that CS obtains the same query token for the same search request is negligible.

Theorem 3. Our ML-RKS or ML-RKS+ guarantees the keyword privacy in the known ciphertext model or known background model.

Proof. ML-RKS or ML-RKS+ guarantees the keyword privacy in the known ciphertext model. This is because the index and query token confidentiality are protected through the secret keys  $(\mathbf{M}_1, \mathbf{M}_2, \mathbf{S})$ . In the ciphertext search process, CS just conducts the inner product operations, which cannot access any information about specific keywords. If more background information is available to CS, the keyword privacy cannot be guaranteed in the known background model.

The final score of ML-RKS or ML-RKS+ is  $\alpha \sum_{j=1}^{m} \nu_{i,j} + \alpha \sum_{j=m+1}^{m+U} \varepsilon_{i,j} + \beta + 1$  or  $\alpha \sum_{j=1}^{m} \nu_{i,j} + \alpha \sum_{j=m+1}^{m+U} \varepsilon_{i,j} + \beta + \theta$ . Assume that the probability of two  $\sum \varepsilon_{i,j}$  with the same value is less than  $1/2^{\varrho}$ , there are at least  $2^{\varrho}$  different values  $\sum \varepsilon_{i,j}$  for each file vector. Note that the number of various  $\sum \varepsilon_{i}$  is not larger than  $UV$ , which has the maximum value on condition that  $U/V = 2$ . We deduce that  $UV \geq UV^{V} = 2^{V}$ , which is greater than  $2^{\varrho}$  when  $U = 2\varrho, V = \varrho$ . Thus, the file vector and query vector should contain at least  $2\varrho$  and  $\varrho$  dummy values respectively, where  $\varrho$  is the system parameter for the tradeoff between security and efficiency. In other words, ML-RKS or ML-RKS+ is secure in the known background model by properly setting  $\varrho$ . Specifically, each  $\varepsilon_{i}$  follows the same distribution ( $\mu' - c, \mu' + c$ ) with the mean value  $\mu'$  and the variance  $\sigma'^{2} = c^{2}/3$ , and the sum of  $\varrho$  independent random variables  $\{\varepsilon_{i}\}$  follows the normal distribution with the mean/variable value ( $\varrho\mu', \varrho c^{2}/3$ ). To make  $\sum \varepsilon_{i}$  follow the same normal distribution  $N(\mu, \sigma^{2})$ , the value  $\mu', \sigma'^{2}$  are set as  $\mu/\varrho, \sigma^{2}/\varrho$ , respectively. The similar security analysis can be referred to scheme [5].

Theorem 4.  $ML-RKS^{+}$ achieves the forward security in the dynamic setting.

Proof. Assume that CS uses previous query tokens to search the newly added files, the permutation matrix will have the same probability  $1 / \tilde{m}$  in both known ciphertext model and known background model. Due to the high probability that the permutation matrix does not match, the search process cannot be conducted correctly. As the permutation matrix

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/76b441327ed780f996c09d0d928ede87d1f9cd783a11748f93db88226dbed15a.jpg)  
Fig. 4. File clustering time.

is independent, CS cannot determine whether various permutation matrices in different versions are the same or not. Thus, CS cannot recognize the same permutation matrix through the statistical analysis over frequent ciphertext retrievals, thereby not breaking the forward security [30].  $\square$

# 7 PERFORMANCE ANALYSIS

In this section, we evaluate the actual performance of ML-RKS or ML-RKS $^+$  through experiments over a real-world dataset-20Newsgroups $^1$ ). This dataset is a collection of approximately 20000 newsgroup documents and partitioned evenly across 20 different newsgroups. The simulation is implemented by utilizing Java in Windows 10 operation system (Inter(R) Core (TM) i7-8565 CPU, 8GB RAM). To evaluate the performance of ML-RKS and ML-RKS $^+$ , we compare them with our schemes without using machine learning, namely basic Ranked Keyword Search (RKS) and Enhanced Ranked Keyword Search  $(\mathrm{RKS}^{+})$ . The tests include file clustering time, indexes generation time, query token generation time, ciphertext search time, file updating time, search accuracy and rank privacy. For simplicity, we set the number of keywords as  $m \in [1,1000]$ , the number of files as  $n \in [1,10000]$ , the number of queried keywords as  $t \in [1,50]$ , the number of top results  $k \in [1,50]$ , the number of clusters as  $p = 5$  and the number of dummy keywords  $U = V = 1$  throughout this paper.

File clustering time. We randomly choose 10000 files from 20Newsgroup dataset and analyze the file vector clustering time by varying variables  $n, m$  in Fig. 4. The theoretical time complexity of file clustering is  $O(nmp)$ . Fig. 4a shows that the file clustering time first grows as the variable  $n$  increases but decreases later with setting  $m = 1000$ , the reason is that the file clustering time is also affected by the number of iterations of k-means clustering algorithm. Fig. 4b shows that the file clustering time increases as the variable  $m$  increases with setting  $n = 10000$ . In addition, we analyze the file clustering time by varying the number of clusters in Fig. 5, e.g.,  $p = 5, 10, 15, 20, 25$ . Fig. 5 shows that the file clustering time increases as the value of  $p$  increases. As part of preprocessing phase, the file clustering incurs additional computation overhead, but it greatly reduces the ciphertext search time and file update time, which will be demonstrated later. Before presenting the practical performance of our schemes without or with the k-means clustering process, we first demonstrate the theoretical complexity of index encryption, token generation and ciphertext search in Table 2. For simplicity, we assume that  $\mathbb{M}_{\mathbf{v}}$  is the same in both basic schemes (e.g., RKS, ML-RKS) and enhanced schemes.

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/49c70ebb6781ae7b8b689e5efa3e402027067f1643cbdbe50394ccd896b5c80d.jpg)  
(a)  $m = 1000$

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/b415e41fe0cb16e59fd02480f4d93e7b7f6c4438b4ab50c91d61dde4c689a53b.jpg)  
Fig. 5. File clustering time,  $n = 10000$ ,  $m = 1000$ .  
(b)  $n = 10000$

TABLE 2 Theoretical Complexities of Our Schemes Without or With kMeans Clustering Process  

<table><tr><td>Schemes</td><td>Encryption comple.</td><td>Token comple.</td><td>Search comple.</td></tr><tr><td>RKS</td><td>(2n-1)Ev</td><td>Ev</td><td>zlog nMv</td></tr><tr><td>ML-RKS</td><td>(2n-1)Ev+ML</td><td>Ev</td><td>zlog LyMv</td></tr><tr><td>RKS+</td><td>2nEv+(2n-1)Mv</td><td>Ev+Emax</td><td>zlog nMv</td></tr><tr><td>ML-RKS+</td><td>2nEv+(2n-1)Mv+ML</td><td>Ev+Emax</td><td>zlog LyMv</td></tr></table>

Notes.  $\mathbb{E}_{\mathbf{v}}$  is the encryption of  $m + U + 2$ -dimension by using the secure  $k$ -NN;  $\mathbb{M}_{\mathbf{v}}$  is the inner product between any two  $m + U + 2$ -dimension vectors;  $\mathbb{E}_{max}$  is the matrix power operation;  $\mathbb{ML}$  is theoretical computation cost of  $k$ -means clustering process.

Indexes generation time. The indexes generation process consists of constructing balanced binary trees for all clusters and encrypting nodes in these trees, and its theoretical time complexity is  $O(nm)$ . We show the indexes generation time of RKS, ML-RKS,  $\mathrm{RKS}^{+}$  and ML- $\mathrm{RKS}^{+}$  schemes in Fig. 6 with varying variables  $n, m$ . Fig. 6a presents the index generation time of the above schemes with setting  $m = 1000$ , which linearly grows with the variable  $n$ . Fig. 6b shows that the indexes generation time grows with the variable  $m$  with setting  $n = 10000$ . From Fig. 6, we notice that ML-RKS and ML- $\mathrm{RKS}^{+}$  have less computation overhead than RKS and  $\mathrm{RKS}^{+}$ . ML- $\mathrm{RKS}^{+}$  (resp.  $\mathrm{RKS}^{+}$ ) incurs slightly higher indexes generation cost than ML-RKS (resp. RKS), as ML- $\mathrm{RKS}^{+}$  (resp.  $\mathrm{RKS}^{+}$ ) needs to generate  $\mathbf{P}_{\text{ver}}$  and conduct dot products between vectors. With the k-means clustering algorithm, ML-RKS and ML- $\mathrm{RKS}^{+}$  reduce the construction time of encrypted balanced binary trees for all clusters. Thus, ML-RKS and ML- $\mathrm{RKS}^{+}$  outperform RKS and  $\mathrm{RKS}^{+}$  schemes in terms of indexes generation.

Query token generation time. We analyze the query token generation time of the above four schemes in Fig. 7. The theoretical time complexity of query token generation is  $O(mt)$ , where  $t$  is the number of queried keywords. Fig. 7a shows the token generation time with setting  $t = 50$ , which linearly grows with the variable  $m$ . Fig. 7b presents the query token

Fig. 6. Index generation time.  
![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/6b43812655f558776e0af5d5008a255392a56e6c1e08978dd37c1139723be30e.jpg)  
Authorized licensed use limited to: East China Normal University. Downloaded on October 13,2025 at 03:06:30 UTC from IEEE Xplore. Restrictions apply.

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/6ebc17e9509e944558f390624afd6130b6a191451dc2e7d8ffeebc2d95b4a131.jpg)  
(a)  $t = 50$

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/2f2023f3c21b27267d98d93f103546f9a3f2c67196347db2e6a43ecbac746f14.jpg)  
(b)  $m = 1000$

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/15a281d9b5e4800b2da2c66c9ea09d1003071ebb814d0d9d79d561259b57bdba.jpg)  
Fig. 7. Search token generation.  
(a)  $k = 10,m = 1000$

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/373fb3c1282a894438988246b1085b1f8dffdbc8a5dc9347fa9a95af7c84c3b7.jpg)  
(b)  $k = 10,n = 10000$

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/ff5d83e8c92f14357e7fddfafbf5c885188a274a832f6c362099dc07466d8c84.jpg)  
Fig. 8. Ciphertext search and file update.  
(c)  $n = 10000, m = 1000$

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/df058342fbd3825cb304c67b32b035c7010c9a3c47bf29946dca4dfe53c0bafe.jpg)  
(d)  $m = 1000$

generation time with setting  $m = 1000$ , which also increases linearly with the variable  $t$ . As the file clustering process does not affect the performance of query token generation, the token generation time of ML-RKS (resp. ML-RKS+) is the same as that of RKS (resp. RKS+). However, ML-RKS+ (resp. RKS+) has slightly higher query token generation overhead due to additional operations such as  $\mathbf{P}_{ver}$ .

Ciphertext search time. The theoretical ciphertext search complexities of ML-RKS, ML-RKS+, RKS and  $\mathrm{RKS^{+}}$  schemes are  $O(nmk)$ . Figs. 8a, 8b and 8c demonstrate the ciphertext search time by varying the variables  $n,m,k$ , respectively. When setting the variables  $k = 10,m = 1000$ , we notice that the ciphertext search time of the above schemes linearly grows with the variable  $n$  in Fig. 8a. As the file modification does not affect the clusters formed, thus the search performance is not affected by it. However, a considerable number of file addition or file deletion operations will affect the number of file vectors in some clusters, thereby affecting the search performance. The similar conclusion can be derived from Figs. 8b and 8c. For example, Fig. 8b (resp. Fig. 8c) shows that the ciphertext search time of the above schemes also increases with the variable  $m$  (resp.  $k$ ) with setting  $k = 10,n = 10000$  (resp.  $m = 1000,n = 10000$ ). This is because the larger  $n$  will increase the height of balanced binary trees, the larger  $m$  incurs much more computation overhead, and the larger  $k$  requires CS to compute more scores. Compared with RKS

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/37a1b300aa569043756e754f8e480d41bbca50c1a4614598f3ee312f6358add1.jpg)  
(a)  $m = 1000$

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/527688e7177b24b6a0e8bf25cda442a923493cd82b7796294e5756381690a238.jpg)  
Fig. 9. Search accuracy and rank privacy.  
(b)  $m = 1000$

and  $\mathrm{RKS^{+}}$  schemes, ML-RKS and  $\mathrm{ML - RKS^{+}}$  significantly reduce the ciphertext search time. Besides, ML-RKS and ML $\mathrm{RKS^{+}}$  have approximately equal computation overhead. The ciphertext search time of ML-RKS and ML $\mathrm{RKS^{+}}$  is less than  $100~\mathrm{ms}$ , thus our proposed schemes can be widely deployed in practical applications.

File update time. To show the performance of file updates in our proposed two schemes, we consider three update operations including file addition, file modification and file deletion in Fig. 8d. As for the file modification or file deletion, its theoretical update complexity is  $O(\log L_y)$ , where  $L_y$  is the number of file vectors in the  $y$ th cluster. The file modification or file deletion needs to update the corresponding sibling node in each height of the balanced binary tree, while the file addition involves many additional nodes. From Fig. 8d, we notice that the update time of file modification or file deletion is much less than that of file addition. Besides, ML-RKS $^+$  is more efficient than RKS $^+$  in terms of file updates. The reason is that the files in the selected cluster in ML-RKS $^+$  are just a small subset of entire files in RKS $^+$ .

Search accuracy. To evaluate the search accuracy of top-  $k$  query results, we use the most common measure  $P_{k} = k^{\prime} / k$ , where  $k^{\prime}$  is the number of real top-  $k$  query results returned by CS. According to the score function  $\alpha (\sum_{j = 1}^{m}\nu_{i,j}\omega_{j} + \sum_{j = 1 + m}^{m + U}\varepsilon_{i,j}) + \beta + 1$  or  $\alpha (\sum_{j = 1}^{m}\nu_{i,j}\omega_{j} + \sum_{j = 1 + m}^{m + U}\varepsilon_{i,j}) + \beta + \theta$  of ML-RKS or ML-RKS $^+$ , the search accuracy is mainly affected by random values  $\sum_{j = 1 + m}^{m + U}\varepsilon_{i,j}$  which follow the normal distribution  $N(\mu ,\sigma^2)$ . We show the search accuracies of RKS/RKS $^+$ , ML-RKS/ML-RKS $^+$  (1) and ML-RKS/ML-RKS $^+$  (5) in Fig. 9a by varying  $k\in [1,50]$  and setting  $m = 1000$ . From Fig. 9a, we notice that the search accuracy is unaffected by the variable  $k$ . However, RKS/RKS $^+$ , ML-RKS/ML-RKS $^+$  (1) and ML-RKS/ML-RKS $^+$  (5) have higher search accuracies when  $\sigma$  is smaller. ML-RKS/ML-RKS $^+$  (1) has lower search accuracy when compared with ML-RKS/ML-RKS $^+$  (5). This is because ML-RKS/ML-RKS $^+$  (1) just selects top- $k$  results from the selected cluster, while ML-RKS/ML-RKS $^+$  (5) selects the top- $k$  results from all clusters without searching all leaf nodes. Fortunately, ML-RKS/ML-RKS $^+$  (5) still can achieve approximately equal search accuracy with RKS/RKS $^+$ . Thus, ML-RKS and ML-RKS $^+$  do not affect the search accuracy while providing efficient ciphertext search. ML-RKS and ML-RKS $^+$  can achieve higher search accuracies with a smaller standard deviation  $\sigma$ , but the DU's rank privacy may be partially leaked to CS. Hence, the parameter  $\sigma$  is a tradeoff between security and search accuracy. It is noted that the file uprate operations do not change the values of parameters  $\sigma, k$ , thus do not affect the performance of search accuracies of our schemes.

Rank privacy. As mentioned above, the smaller  $\sigma$  will improve the search accuracy, but it will leak the rank privacy. In other words, the smaller  $\sigma$  will lead to the leakage of rank privacy such as the sequence of ranked query results. Hence, the practical ML-RKS or ML-RKS $^+$  should hide the rank order of returned results as much as possible. To evaluate the rank privacy, we define the rank perturbation as  $\widetilde{p}_i = |r_i - r_i'|$  used in [5], where  $r_i$  is the rank number of file  $f_i$  in the top- $k$  results and  $r_i'$  is the rank number of  $f_i$  in the real top- $k$  results. Then, the rank privacy of top- $k$  results can be defined as  $\widetilde{P}_k = \sum \widetilde{p}_i / k$ . In Fig. 9b, the rank privacy is higher when setting a larger  $\sigma$ . Besides, the ML-RKS/ML-RKS $^+$ (1) has higher rank privacy when compared with ML-RKS/ML-RKS $^+$ (5), and ML-RKS/ML-RKS $^+$ (5) has the similar rank privacy with RKS/RKS $^+$ . Hence, the parameter  $\sigma$  is a tradeoff between rank privacy and search accuracy, which allows DUs to flexibly satisfy various requirements in practice by adjusting the value of  $\sigma$ .

# 8 CONCLUSION

In this paper, we first construct the balanced binary tree-based indexes by using the k-means clustering algorithm to boost the search efficiency in ML-RKS, then avoid the leakage of forward privacy by generating a permutation matrix in  $\mathrm{ML - RKS^{+}}$ . Both ML-RKS and  $\mathrm{ML - RKS^{+}}$  achieve expressive search by allowing DUs to specify weight values for queried keywords. Besides, our proposed schemes do not lower search accuracy while providing an efficient ciphertext search. We also analyze that ML-RKS and  $\mathrm{ML - RKS^{+}}$  meet the designed privacy requirements, dynamic update with forward security and efficiency. We provide empirical experiments using a real-world dataset to evaluate search efficiency, search accuracy and rank privacy.

# REFERENCES

[1] C. Ge, W. Susilo, Z. Liu, J. Xia, P. Szalachowski, and F. Liming, "Secure keyword search and data sharing mechanism for cloud computing," IEEE Trans. Dependable Secure Comput., vol. 18, no. 6, pp. 2787-2800, Nov./Dec. 2020.  
[2] D. X. Song, D. Wagner, and A. Perrig, "Practical techniques for searches on encrypted data," in Proc. IEEE Symp. Secur. Privacy, 2000, pp. 44-55.  
[3] D. Boneh, G. Di Crescenzo, R. Ostrovsky, and G. Persiano, "Public key encryption with keyword search," in Proc. Int. Conf. Theory Appl. Cryptogr. Techn., 2004, pp. 506-522.  
[4] C. Wang, N. Cao, K. Ren, and W. Lou, "Enabling secure and efficient ranked keyword search over outsourced cloud data," IEEE Trans. Parallel Distrib. Syst., vol. 23, no. 8, pp. 1467-1479, Aug. 2011.  
[5] N. Cao, C. Wang, M. Li, K. Ren, and W. Lou, "Privacy-preserving multi-keyword ranked search over encrypted cloud data," IEEE Trans. Parallel Distrib. Syst., vol. 25, no. 1, pp. 222-233, Jan. 2013.  
[6] Z. Fu, X. Wu, C. Guan, X. Sun, and K. Ren, "Toward efficient multi-keyword fuzzy search over encrypted outsourced data with accuracy improvement," IEEE Trans. Inf. Forensics Secur., vol. 11, no. 12, pp. 2706-2716, Dec. 2016.  
[7] W. Zhang, Y. Lin, S. Xiao, J. Wu, and S. Zhou, "Privacy preserving ranked multi-keyword search for multiple data owners in cloud computing," IEEE Trans. Comput., vol. 65, no. 5, pp. 1566-1577, May 2015.  
[8] Z. Fu, X. Sun, N. Linge, and L. Zhou, "Achieving effective cloud search services: Multi-keyword ranked search over encrypted cloud data supporting synonym query," IEEE Trans. Consum. Electron., vol. 60, no. 1, pp. 164-172, Feb. 2014.  
[9] Z. Xia, X. Wang, X. Sun, and Q. Wang, "A secure and dynamic multi-keyword ranked search scheme over encrypted cloud data," IEEE Trans. Parallel Distrib. Syst., vol. 27, no. 2, pp. 340-352, Feb. 2015.

[10] W. Zhang, S. Xiao, Y. Lin, T. Zhou, and S. Zhou, "Secure ranked multi-keyword search for multiple data owners in cloud computing," in Proc. Annu. IEEE/IFIP Int. Conf. Dependable Syst. Netw., 2014, pp. 276-286.  
[11] S. Kamara, C. Papamanthou, and T. Roeder, "Dynamic searchable symmetric encryption," in Proc. ACM Conf. Comput. Commun. Secur., 2012, pp. 965-976.  
[12] Y. Zhang, J. Katz, and C. Papamanthou, "All your queries are belong to us: The power of file-injection attacks on searchable encryption," in Proc. USENIX Secur. Symp., 2016, pp. 707-720.  
[13] T. Kanungo, D. M. Mount, N. S. Netanyahu, C. D. Piatko, R. Silverman, and A. Y. Wu, "An efficient k-means clustering algorithm: Analysis and implementation," IEEE Trans. Pattern Anal. Mach. Intell., vol. 24, no. 7, pp. 881-892, Jul. 2002.  
[14] B. Wang, S. Yu, W. Lou, and Y. T. Hou, "Privacy-preserving multi-keyword fuzzy search over encrypted data in the cloud," in Proc. IEEE Conf. Comput. Commun., 2014, pp. 2112-2120.  
[15] Y. Yang, Y.-C. Zhang, J. Liu, X.-M. Liu, F. Yuan, and S.-P. Zhong, "Chinese multi-keyword fuzzy rank search over encrypted cloud data based on locality-sensitive hashing," J. Inf. Sci. Eng., vol. 35, no. 1, pp. 137-158, 2019.  
[16] Z. Fu, F. Huang, X. Sun, A. Vasilakos, and C.-N. Yang, "Enabling semantic search based on conceptual graphs over encrypted outsourced data," IEEE Trans. Serv. Comput., vol. 12, no. 5, pp. 813-823, 2016.  
[17] Z. Fu, X. Wu, Q. Wang, and K. Ren, "Enabling central keyword-based semantic extension search over encrypted outsourced data," IEEE Trans. Inf. Forensics Secur., vol. 12, no. 12, pp. 2986-2997, Dec. 2017.  
[18] C. Guo, X. Chen, Y. Jie, F. Zhangjie, M. Li, and B. Feng, "Dynamic multi-phrase ranked search over encrypted data with symmetric searchable encryption," IEEE Trans. Serv. Comput., vol. 13, no. 6, pp. 1034-1044, Nov./Dec. 2017.  
[19] Q. Liu, Y. Tian, J. Wu, T. Peng, and G. Wang, "Enabling verifiable and dynamic ranked search over outsourced data," IEEE Trans. Services Comput., to be published, doi:10.1109/TSC.2019.2922177.  
[20] X. Jiang, J. Yu, J. Yan, and R. Hao, "Enabling efficient and verifiable multi-keyword ranked search over encrypted cloud data," Inf. Sci., vol. 403, pp. 22-41, 2017.  
[21] J. Bethencourt, A. Sahai, and B. Waters, "Ciphertext-policy attribute-based encryption," in Proc. IEEE Symp. Secur. Privacy, 2007, pp. 321-334.  
[22] M. Naveed, M. Prabhakaran, and C. A. Gunter, "Dynamic searchable encryption via blind storage," in Proc. IEEE Symp. Secur. Privacy, 2014, pp. 639-654.  
[23] H. Li, D. Liu, Y. Dai, T. H. Luan, and X. S. Shen, "Enabling efficient multi-keyword ranked search over encrypted mobile cloud data through blind storage," IEEE Trans. Emerg. Topics Comput., vol. 3, no. 1, pp. 127-138, Mar. 2014.  
[24] C. Chen et al., "An efficient privacy-preserving ranked keyword search method," IEEE Trans. Parallel Distrib. Syst., vol. 27, no. 4, pp. 951-963, Apr. 2015.  
[25] R. Zhao and M. Iwaihara, "Lightweight efficient multi-keyword ranked search over encrypted cloud data using dual word embeddings," 2017, arXiv:1708.09719.  
[26] R. Bost, "oφoc; Forward secure searchable encryption," in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., 2016, pp. 1143-1154.  
[27] R. Bost, B. Minaud, and O. Ohrimenko, "Forward and backward private searchable encryption from constrained cryptographic primitives," in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., 2017, pp. 1465-1482.  
[28] X. Song, C. Dong, D. Yuan, Q. Xu, and M. Zhao, "Forward private searchable symmetric encryption with optimized i/o efficiency," IEEE Trans. Dependable Secure Comput., vol. 17, no. 5, pp. 912-927, Sep./Oct. 2018.  
[29] S.-F. Sun et al., "Practical backward-secure searchable encryption from symmetric puncturable encryption," in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., 2018, pp. 763-780.  
[30] A. Najafi, H. H. S. Javadi, and M. Bayat, "Verifiable ranked search over encrypted data with forward and backward privacy," Future Gener. Comput. Syst., vol. 101, pp. 410-419, 2019.  
[31] W. K. Wong, D. W.-L. Cheung, Cheung, B. Kao, and N. Mamoulis, "Secure kNN computation on encrypted databases," in Proc. ACM SIGMOD Int. Conf. Manage. Data, 2009, pp. 139-152.

[32] G. Liu, G. Yang, S. Bai, H. Wang, and Y. Xiang, "FASE: A fast and accurate privacy-preserving multi-keyword top-k retrieval scheme over encrypted cloud data," IEEE Trans. Serv. Comput., to be published, doi:10.1109/TSC.2020.3023393.  
[33] W. Sun et al., "Verifiable privacy-preserving multi-keyword text search in the cloud supporting similarity-based ranking," IEEE Trans. Parallel Distrib. Syst., vol. 25, no. 11, pp. 3025-3035, Nov. 2013.  
[34] J. Li et al., "Verifiable semantic-aware ranked keyword search in cloud-assisted edge computing," IEEE Trans. Services Comput., to be published, doi:10.1109/TSC.2021.3098864.  
[35] X. Dai, H. Dai, C. Rong, G. Yang, and F. Xiao, "Enhanced semantic-aware multi-keyword ranked search scheme over encrypted cloud data," IEEE Trans. Cloud Comput., to be published, doi:10.1109/TCC.2020.3047921.  
[36] Q. Liu, Y. Peng, S. Pei, J. Wu, T. Peng, and G. Wang, "Prime inner product encoding for effective wildcard-based multi-keyword fuzzy search," IEEE Trans. Services Comput., to be published, doi:10.1109/TSC.2020.3020688.  
[37] H. Zhang, S. Zhao, Z. Guo, Q. Wen, W. Li, and F. Gao, "Scalable fuzzy keyword ranked search over encrypted data on hybrid clouds," IEEE Trans. Cloud Comput., to be published, doi:10.1109/TCC.2021.3092358.  
[38] X. Ding, P. Liu, and H. Jin, "Privacy-preserving multi-keyword top-k similarity search over encrypted data," IEEE Trans. Dependable Secure Comput., vol. 16, no. 2, pp. 344-357, Mar./Apr. 2017.  
[39] E. Stefanov et al., "Path ORAM: An extremely simple oblivious RAM protocol," in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., 2013, pp. 299-310.  
[40] N. Gilboa and Y. Ishai, "Distributed point functions and their applications," in Proc. Annu. Int. Conf. Theory Appl. Cryptogr. Techn., 2014, pp. 640-658.  
[41] A. Likas, N. Vlassis, and J. J. Verbeek, "The global k-means clustering algorithm," Pattern Recognit., vol. 36, no. 2, pp. 451-461, 2003.  
[42] J. Yuan, S. Yu, and L. Guo, "SEISA: Secure and efficient encrypted image search with access control," in Proc. IEEE Conf. Comput. Commun., 2015, pp. 2083-2091.  
[43] C. Zuo, S.-F. Sun, J. K. Liu, J. Shao, and J. Pieprzyk, "Dynamic searchable symmetric encryption schemes supporting range queries with forward (and backward) security," in Proc. Eur. Symp. Res. Comput. Secur., 2018, pp. 228-246.  
[44] M. D. Green and I. Miers, "Forward secure asynchronous messaging from puncturable encryption," in Proc. IEEE Symp. Secur. Privacy, 2015, pp. 305-320.  
[45] C. Yang, W. Zhang, J. Xu, J. Xu, and N. Yu, "A fast privacy-preserving multi-keyword search scheme on cloud data," in Proc. Int. Conf. Cloud Service Comput., 2012, pp. 104-110.  
[46] L. Chen, L. Qiu, K.-C. Li, W. Shi, and N. Zhang, "DMRS: An efficient dynamic multi-keyword ranked search over encrypted cloud data," Soft. Comput., vol. 21, no. 16, pp. 4829-4841, 2017.

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/1a333de6a44e896d4c8dc53697bf8c1226b626d8df565eed1425015661e46891.jpg)

Yinbin Miao (Member, IEEE) received the BE degree with the Department of Telecommunication Engineering from Jilin University, Changchun, China, in 2011 and the PhD degree with the Department of Telecommunication Engineering from Xidian University, Xi'an, China, in 2016. From September 2018 to September 2019, he was a postdoctor with Nanyang Technological University and a postdoctor with the City University of Hong Kong. He is currently an associate professor with the Department of Cyber Engi

neering, Xidian University, Xi'an, China. His research interests include information security and applied cryptography.

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/05aeb2cb688aa927d023b45d93b7601ba15e45d005c74b5dbe967ed7dc047bf1.jpg)

Wei Zheng received the BE degree with the Department of Information Security from Nanchang University, Nanchang, China, in 2020. He is currently working toward the ME degree with the Department of Cyber Engineering, Xidian University, Xi'an, China. His research interests include information security and applied cryptography.

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/64bfc314c1bb1c5dcc05a74a914aef60cfbcea947e6f7fa27c007f93f7110073.jpg)

Xiaohua Jia (Fellow, IEEE) received the BSc degree in 1984 and MEng degree from the University of Science and Technology of China in 1987, and the DSc degree in 1991 in information science from the University of Tokyo. He is currently a chair professor with the Dept of Computer Science, City University of Hong Kong. His research interests include cloud computing and distributed systems, computer networks and mobile computing. He is currently the editor of IEEE Internet of Things, IEEE Transactions on Parallel and Distributed Sys

tems (2006-2009), Wireless Networks, Journal of World Wide Web, and Journal of Combinatorial Optimization. He is the general chair of ACM MobiHoc 2008, the TPC co-chair of IEEE GlobeCom 2010 Ad Hoc and sensor networking symposium, and the areachair of IEEE INFOCOM 2010 and 2015.

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/3ce07714993968abe20c0b96fdece370bfc208e31fd84b24fc448b3cb2e243a0.jpg)

Ximeng Liu (Member, IEEE) received the PhD degree with the Department of Telecommunication Engineering from Xidian University, Xi'an, China, in 2015. He is currently a professor with the Key Laboratory of Information Security of Network Systems, College of Mathematics and Computer Science, Fuzhou University, Fuzhou, China. His research interests include applied cryptography and Big Data security.

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/cdda39bef4b2e40aaf69da152244621976adf5814e976f7c1f72ab515c0cd8f0.jpg)

Kim-Kwang Raymond Choo (Senior Member, IEEE) received the PhD degree in information security in 2006 from the Queensland University of Technology, Australia. He is currently the cloud technology endowed professor with The University of Texas, San Antonio (UTSA). He was the recipient of the UTSA College of Business Col. Jean Piccione and Lt. Col. Philip Piccione Endowed Research Awards for Tenured Faculty in 2018, IEEE TrustCom 2018, and ESORICS 2015 best paper awards. He is also an Australian Computer Society fellow.

![](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/f9660220bbba69f61f382327662a51e3b0c624b1e6f01c4a468b95b1c9418e86.jpg)

Robert H. Deng (Fellow, IEEE) is currently an AXA chair professor of Cybersecurity and professor of information systems with the School of Information Systems, Singapore Management University since 2004. His research interests include data security and privacy, multimedia security, network, and system security. He was or is currently with the editorial boards of many international journals, including IEEE Transactions on Information Forensics and Security and IEEE Transactions on Dependable and Secure Computing. He was the recipient of the

Distinguished Paper Award (NDSS 2012), Best Paper Award (CMS 2012), and Best Journal Paper Award (IEEE Communications Society 2017).

For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/csdl.