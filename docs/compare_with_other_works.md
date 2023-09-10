# Comparing with other works

An Approach to Identify Source Code Files Impacted by Architectural Technical Debt (ATD) using our method and comparing with existing methods Sas et al. 2022 (https://onlinelibrary.wiley.com/doi/full/10.1002/smr.2398) and Tsoukalas et al. 2023 (https://onlinelibrary.wiley.com/doi/full/10.1002/smr.2564), already validated by the scientific community. Below is a detailed overview of our plan:

![Planning](https://raw.githubusercontent.com/armandossrecife/piloto/main/docs/diagramas/ATDCodeAnalyzer.png "Planning to compare with other works")

## 1. The Proposed Method (m1)

### 1.1 Identification of ATD-Impacted source code files using change analysis and code metrics:

Our method is divided into five phases:

Phase 1 - Given a git repository, extract historical commit data and modified files in each commit.

Phase 2 - Select the source code files impacted by Architectural Smells and calculate metrics ((AMLOC - Accumulated LOC of each source code file over time), (FOC - frequency of commit occurrence for each source code file), and (CC - cyclomatic complexity of each source code file)).

Phase 3 - Calculate quartiles of the metrics and select the source code files impacted by Architectural Smells (Cyclic Dependency and Hub-like Dependency). In this phase, tools such as Arcan are used to identify Architectural Smells, and DesigniteJava is used to identify Design Smells.

Phase 4 - Analyze critical source code files impacted by Architectural Smells and their dependent source code files with co-change. The dependent source code files are selected using DSM (Dependency Structure Matrix)

Phase 5 - Report potential critical source code files impacted by Architectural Smells.

More details in https://github.com/mining-software-repositories/cassandra/blob/main/data/AnalysisCassandraRepositoryFlow.png

### 1.1.2 Repository Details

| name             | url                                               |qtd_files |   LOC_files | qtd_java |   LOC_java |   qtd_commits |   qtd_releases |   life_span (years) | source_java                 |   stars |   forks |   colaborators |
|:-----------------|:--------------------------------------------------|--------:|------------:|-------:|-----------:|--------------:|---------------:|------------:|:----------------------------|--------:|--------:|---------------:|
| activemq         | https://github.com/apache/activemq.git            |    4927 |      466219 |   4360 |     416555 |         11476 |             85 |     17.75 | activemq-http/src/main/java |    2200 |    1400 |            127 |
| cassandra        | https://github.com/apache/cassandra.git           |    4999 |     1055614 |   4460 |     680880 |         29140 |            297 |     14.52 | src/java                    |    8100 |    3400 |            424 |
| guava            | https://github.com/google/guava.git               |    1968 |      358412 |   1909 |     354072 |          6173 |            101 |     14.23 | guava/src                   |   48100 |   10700 |            293 |
| jackson-databind | https://github.com/FasterXML/jackson-databind.git |    1194 |      202811 |   1153 |     147890 |          7180 |            187 |     11.72 | src/main/java               |    3300 |    1300 |            225 |
| kafka            | https://github.com/apache/kafka.git               |    5434 |      856923 |   4269 |     629799 |         11650 |            222 |     12.11 | core/src                    |   25700 |   13000 |           1042 |

### 1.2 Testing method on selectect repositories: 

1.2.1 Testing on Apache Cassandra Repository (https://github.com/apache/cassandra):

The outcome of our tests on the Cassandra repository is a set of critical files affected by ATD and the files dependent on these critical files.

1.2.2 Testing on Apache Kafka Repository (https://github.com/apache/kafka):

The outcome of our tests on the Kafka repository is a set of critical files affected by ATD and the files dependent on these critical files.

1.2.3 Testing on Apache ActiveMQ Repository (https://github.com/apache/activemq):

The outcome of our tests on the ActiveMQ repository is a set of critical files affected by ATD and the files dependent on these critical files.

1.2.4 Testing on Apache Guava Repository (https://github.com/google/guava):

The outcome of our tests on the Guava repository is a set of critical files affected by ATD and the files dependent on these critical files.

1.2.5 Testing on Apache Jackson-databind Repository (https://github.com/FasterXML/jackson-databind.git)

The outcome of our tests on Jackson-databind repository is a set of critical files affected by ATD and the files dependent on these critical files.

## 2. Comparison of Results from the proposed method and Sas et al. 2022 (m2)

More details in [comparing_sas2022](https://github.com/armandossrecife/piloto/blob/main/notebooks/compare_with_sas2022.ipynb)

### 2.1 Comparison with Sas et al. 2022 (m2):

2.1.1 We compared the critical source code files identified by our method with the files impacted by Architectural Smells (Cyclic Dependency and Hub-like Dependency) identified in Sas et al. 2022's work.

2.1.2 In addition to the Cassandra repository, three more repositories analyzed by Sas et al. 2022's work were selected: ActiveMQ, Guava and Jackson-databind. These selected projects were chosen because they have a large number of .java files (>1500 files), a substantial LOC count for .java files (>300000 lines of code), project lifespan exceeding 10 years, a high number of project commits (>5000 commits), numerous releases (>80 releases), and significant community involvement (>2000 stars and >1000 forks of the  and coloborators > 120).

The objective of comparing the results obtained using our method with the methods of Sas et al. 2022 and Tsoukalas et al. 2023 is to demonstrate that our method produces results that are close to or consistent with those already validated by the scientific community.

R1) Data from the SAS2022 was collected regarding classes affected by Architectural Smells from the following repositories:

List of Critical Classes m1 x m2 - It shows the names of the critical classes identified by each method.
```bash
Repository  | ATDCodeAnalyzer                           | SAS2022
Cassandra   | list_cassandra_critical_m1 		| list_cassandra_critical_m2
ActiveMQ    | list_activemq_critical_m1 		| list_activemq_critical_m2
Guava       | list_guava_critical_m1 		  	| list_guava_critical_m2
Jackson     | list_jackson_critical_m1                  | list_jackson_critical_m2
```

Comparison of Methods - It shows the number of classes identified as critical by each method, as well as the accuracy rate of ATDCodeAnalyzer in relation to SAS2022.
```bash
Repository 	| ATDCodeAnalyzer | SAS2022 	| ATDCodeAnalyzer Hit Rate in relation to SAS2022
Cassandra 	| 12                | 11 		| 91.66%
ActiveMQ        | 5                 | 3 		| 60%
Guava           | 46                | 27 		| 59%
Jackson         | 8                 | 4                 | 50%
```

**Cassandra**

list_cassandra_critical_m1 = ['StorageService', 'ColumnFamilyStore', 'DatabaseDescriptor', 'CompactionManager', 'StorageProxy', 'SSTableReader', 'Config', 'CassandraDaemon', 'SelectStatement', 'SinglePartitionReadCommand', 'NodeProbe', 'MessagingService']

list_cassandra_critical_m2 = ['StorageService', 'ColumnFamilyStore', 'DatabaseDescriptor', 'CompactionManager', 'StorageProxy', 'SSTableReader', 'Config', 'CassandraDaemon', 'SelectStatement', 'SinglePartitionReadCommand', 'MessagingService']

![Cassandra M1 x M2](https://raw.githubusercontent.com/armandossrecife/piloto/main/docs/diagramas/cassandram1xm2.png "Cassandra M1 x M2")

**ActiveMQ**

list_activemq_critical_m1 = ['BrokerService','DemandForwardingBridgeSupport','Queue','TopicSubscription','TransportConnector']

list_activemq_critical_m2 = ['BrokerService', 'Queue', 'TransportConnector']

![AcitveMQ M1 x M2](https://raw.githubusercontent.com/armandossrecife/piloto/main/docs/diagramas/activemqm1xm2.png "ActiveMQ M1 x M2")

**Guava** 

list_guava_critical_m1 = ['AbstractFuture', 'BaseEncoding', 'CacheBuilder', 'CacheBuilderSpec', 'ClassPath', 'ClosingFuture', 'Converter', 'Doubles', 'Equivalence', 'ExecutionSequencer', 'Floats', 'Hashing', 'ImmutableBiMap', 'ImmutableCollection', 'ImmutableList', 'ImmutableListMultimap', 'ImmutableMap', 'ImmutableMultimap', 'ImmutableMultiset', 'ImmutableRangeMap', 'ImmutableRangeSet', 'ImmutableSet', 'ImmutableSetMultimap', 'ImmutableSortedMap', 'ImmutableSortedSet', 'ImmutableTable', 'InterruptibleTask', 'Ints', 'Iterables', 'Iterators', 'LocalCache', 'LongMath', 'Longs', 'MapMakerInternalMap', 'Maps', 'Multisets', 'Ordering', 'Platform', 'Range', 'RegularImmutableMap', 'Sets', 'Synchronized', 'TreeRangeSet', 'TypeToken', 'Types', 'ValueGraphBuilder']

list_guava_critical_m2 = ['BaseEncoding', 'CacheBuilder', 'CacheBuilderSpec', 'ClassPath', 'ImmutableBiMap', 'ImmutableList', 'ImmutableListMultimap', 'ImmutableMap', 'ImmutableMultimap', 'ImmutableMultiset', 'ImmutableRangeMap', 'ImmutableRangeSet', 'ImmutableSet', 'ImmutableSetMultimap', 'ImmutableSortedMap', 'ImmutableSortedSet', 'ImmutableTable', 'LocalCache', 'MapMakerInternalMap', 'Maps', 'Ordering', 'Platform', 'Range', 'RegularImmutableMap', 'Sets', 'TreeRangeSet', 'TypeToken']

![Guava M1 x M2](https://raw.githubusercontent.com/armandossrecife/piloto/main/docs/diagramas/guavam1xm2.png "Guava M1 x M2")

**Jackson-databind**

 list_jackson_critical_m1  = ['AnnotationIntrospector', 'AnnotationIntrospectorPair', 'ClassUtil', 'EnumValues', 'JsonNode', 'ObjectMapper', 'ObjectNode', 'TokenBuffer']

 list_jackson_critical_m2 = ['AnnotationIntrospector', 'JsonNode', 'ObjectMapper', 'ObjectNode']

![Jackson-databind M1 x M2](https://raw.githubusercontent.com/armandossrecife/piloto/main/docs/diagramas/jacksonm1xm2.png "Jackson-databind M1 x M2")

Obs: 
- Explain the comparison process between the critical source code files identified by your method and those impacted by Architectural Smells in Sas et al. 2022's work.

### 2.2 Specific Comparisons (TODO):

2.2.1 Provide a detailed explanation of the comparison process for each of the repositories: ActiveMQ and Guava.

2.2.2 Describe the process of executing your method on these repositories and comparing the results with Sas et al.'s method (SASM).

## 3. Testing and Comparison with Tsoukalas et al. 2023 (m3) on the Kafka Repository:

3.1 Describe how you applied your method to conduct tests on the Kafka repository (TODO).

3.2 Explain how the results were used to compare with Tsoukalas et al. 2023's work on technical debt prioritization.

3.2. Highlight the focus on classes with the highest prioritization of technical debt payments.

R2. Data from the TKS2023 work were collected in relation to the most critical classes and those with the highest priority for DT payment:

List of Critical Classes m1 x m3
```bash
Repository | ATDCodeAnalyzer       | TKS2023
Kafka      | list_kafka_critical_m1 | list_kafka_critical_m3
Guava      | list_guava_critical_m1 | list_guava_critical_m3
```

Comparison of Methods
```bash
Repository | ATDCodeAnalyzer | TKS2023 | ATDCodeAnalyzer Hit Rate in relation to TKS2023
Kafka      | 18              | 9       | 50.00%
Guava      | 16              | 8       | 50.00%
```

**Kafka**

list_kafka_critical_m1 = ['StreamThread.java','Fetcher.java','StreamTask.java','KafkaConsumer.java','StreamsConfig.java','ConsumerCoordinator.java','KafkaProducer.java','KafkaStreams.java','RocksDBStore.java','KTableImpl.java','AbstractCoordinator.java','KStreamImpl.java','ProcessorStateManager.java','NetworkClient.java','Sender.java','Utils.java','ConsumerNetworkClient.java','RecordAccumulator.java']

list_kafka_critical_m2 = ['StreamThread.java', 'KafkaConsumer.java', 'StreamTask.java', 'Fetcher.java', 'KafkaStreams.java','KStreamImpl.java', 'KafkaProducer.java','StreamsConfig.java', 'ConsumerCoordinator.java']

![Kafka M1 x M3](https://raw.githubusercontent.com/armandossrecife/piloto/main/docs/diagramas/kafkam1xm3.png "Kafka M1 x M3")

**Guava**

list_guava_critical_m1 =['Graphs.java','AbstractFuture.java','Futures.java','Maps.java','AbstractNetwork.java','ImmutableMultiset.java','ImmutableSet.java','Iterators.java','MoreFiles.java','LocalCache.java', 'ImmutableMap.java','ImmutableCollection.java','MapMakerInternalMap.java','Sets.java','HttpHeaders.java', 'ImmutableNetwork.java']

list_guava_critical_m2 = ['Maps.java','ImmutableMap.java', 'LocalCache.java', 'AbstractFuture.java', 'HttpHeaders.java', 'Futures.java', 'Sets.java', 'MapMakerInternalMap.java']

![Guava M1 x M3](https://raw.githubusercontent.com/armandossrecife/piloto/main/docs/diagramas/guavam1xm3.png "Guava M1 x M3")

More details in [compare_with_tks2023](https://github.com/armandossrecife/piloto/blob/main/notebooks/compare_with_tks_2023.ipynb)

## 4. Comparing Features among M1, M2 and M3

| Id | Feature | ATDCodeAnalyzer (M1) | SAS2022 (M2) | TKS2023 (M3) |
|:---|:--------|:---------------------|-------------:|-------------:|
| 1 | Github Repository        		 | Yes              | Yes           | Yes |
| 2 | Code Metrics             		 | LOC (Lines of Code), AMLOC (Code Churn),FOC,CC | LOC, Change Has Occurred (CHO),<br/>Percentage of Commits a Class has Changed (PCCC),TACH (Code Churn)  | reliability_remediation_effort,reliability_rating,<br/>bugs,security_remediation_effort,security_rating,<br/>vulnerabilities,<br/>sqale_debt_ratio,sqale_rating,<br/>code_smells,sqale_index,<br/>development_cost,<br/>effort_to_reach_maintainability_rating_a,<br/>test_failures,coverage,test_errors,line_coverage,<br/>lines_to_cover,uncovered_lines,test_success_density,<br/>skipped_tests,duplicated_files,duplicated_blocks,<br/>duplicated_lines,duplicated_lines_density,statements,<br/>functions,generated_lines,lines,comment_lines,<br/>ncloc,comment_lines_density,complexity,<br/>cognitive_complexity,file_complexity,major_violations,<br/>blocker_violations,info_violations,violations,<br/>critical_violations,reopened_issues,<br/>false_positive_issues,confirmed_issues,open_issues,<br/>wont_fix_issues,minor_violations,<br/>public_undocumented_api,<br/>public_documented_api_density,<br/>Ca,Ce,WMC,NOC,DIT,LCOM,CBO,NPM,RFC |
| 3 | Analysis of code changes over time | Yes | Yes | Yes |
| 4 | Architectural Smells     		 | Cyclic Dependency,<br/>Hub-Like Dependency | Cyclic Dependency, Unstable Dependency,<br/> Hub-Like Dependency, God Component | No |
| 5 | Design Smells               | Yes              | No    | No |
| 6 | Code Smells                 | No               | No    | Yes |
| 7 | Analysis of Quartiles    	     | Yes              | Yes   | No |
| 8 | Dependency Structure Matrix    | Yes              | No    | No |
| 9 | Critical Classes               | Yes              | Partial    |Yes |
| 10 | Co-change                      | Yes              | No    | No |
| 11 | Files impacted by Critical Class | Yes            | No    | No |
| 12 | Analysis of Issue Tracker      | No               | No    | Yes |
| 13 | Machine Learning               | No               | No    | Yes |
| 14 | Change Proneness               | Yes              | No    | Yes |
| 15 | TD change Proneness            | No               | No    | Yes |
| 16 | Arcan                          | Yes              | Yes   | No |
| 17 | Sonarqube                      | No               | No    | Yes |
| 18| CK Java                        | No               | No    | Yes |
| 19 | TD Forecast                    | No               | No    | Yes |
| 20 | Result visualization           | Yes              | No    | Yes |
| 21 | Automatic Process              | Yes              | No    | No  |

This table is available on spreadsheet https://github.com/armandossrecife/piloto/blob/main/docs/ComparingFeaturesAmongM1M2M3.xlsx
