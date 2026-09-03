import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// Sidebar mirrors site/docs.json so the two builds stay in step.
const sidebar = [
  {
    "label": "Start here",
    "collapsed": true,
    "items": [
      {
        "label": "Orientation",
        "collapsed": true,
        "items": [
          {
            "slug": ""
          },
          {
            "slug": "start/how-this-works"
          },
          {
            "slug": "start/three-layers"
          },
          {
            "slug": "start/who-this-is-for"
          },
          {
            "slug": "start/about-the-numbers"
          },
          {
            "slug": "start/setup"
          },
          {
            "slug": "start/how-to-study"
          }
        ]
      },
      {
        "label": "The map",
        "collapsed": true,
        "items": [
          {
            "slug": "start/curriculum-map"
          },
          {
            "slug": "start/portfolio"
          },
          {
            "slug": "start/faq"
          }
        ]
      }
    ]
  },
  {
    "label": "Phase 1 · Foundations",
    "collapsed": true,
    "items": [
      {
        "label": "Week 1 — Algorithmic Thinking & Memory Foundations (C)",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-01"
          },
          {
            "slug": "curriculum/p1/week-01/1-how-a-computer-represents-everything"
          },
          {
            "slug": "curriculum/p1/week-01/2-from-source-code-to-running-process"
          },
          {
            "slug": "curriculum/p1/week-01/3-stack-heap-and-pointers"
          },
          {
            "slug": "curriculum/p1/week-01/4-algorithms-asymptotic-complexity"
          },
          {
            "slug": "curriculum/p1/week-01/5-correctness-debugging-memory-safety-tooling"
          },
          {
            "slug": "curriculum/p1/week-01/lab"
          }
        ]
      },
      {
        "label": "Week 2 — Terminal Literacy, Version Control & Vim",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-02"
          },
          {
            "slug": "curriculum/p1/week-02/1-the-shell-filesystem-as-a-system"
          },
          {
            "slug": "curriculum/p1/week-02/2-text-processing-pipelines"
          },
          {
            "slug": "curriculum/p1/week-02/3-bash-scripting-automation"
          },
          {
            "slug": "curriculum/p1/week-02/4-git-the-model-not-the-commands"
          },
          {
            "slug": "curriculum/p1/week-02/5-ssh-keys-remote-work-vim-survival"
          },
          {
            "slug": "curriculum/p1/week-02/lab"
          }
        ]
      },
      {
        "label": "Week 3 — Python Core & Object-Oriented Design",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-03"
          },
          {
            "slug": "curriculum/p1/week-03/1-python-s-model-objects-names-memory"
          },
          {
            "slug": "curriculum/p1/week-03/2-data-structures-and-complexity-in-practice"
          },
          {
            "slug": "curriculum/p1/week-03/3-functions-errors-and-the-standard-library"
          },
          {
            "slug": "curriculum/p1/week-03/4-object-oriented-design-done-properly"
          },
          {
            "slug": "curriculum/p1/week-03/5-professional-python-typing-testing-tooling-packaging"
          },
          {
            "slug": "curriculum/p1/week-03/lab"
          }
        ]
      },
      {
        "label": "Week 4 — Concurrency, Parallelism & `asyncio`",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-04"
          },
          {
            "slug": "curriculum/p1/week-04/1-concurrency-vs-parallelism-vs-the-gil"
          },
          {
            "slug": "curriculum/p1/week-04/2-threads-and-shared-state"
          },
          {
            "slug": "curriculum/p1/week-04/3-processes-and-true-parallelism"
          },
          {
            "slug": "curriculum/p1/week-04/4-asyncio-the-event-loop-from-first-principles"
          },
          {
            "slug": "curriculum/p1/week-04/5-reliability-patterns-for-i-o-heavy-systems"
          },
          {
            "slug": "curriculum/p1/week-04/lab"
          }
        ]
      },
      {
        "label": "Week 5 — Web Plumbing — HTTP, HTML, CSS, ES6",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-05"
          },
          {
            "slug": "curriculum/p1/week-05/1-how-the-web-actually-works"
          },
          {
            "slug": "curriculum/p1/week-05/2-html5-semantic-structure"
          },
          {
            "slug": "curriculum/p1/week-05/3-css-responsive-layout"
          },
          {
            "slug": "curriculum/p1/week-05/4-modern-javascript-es6"
          },
          {
            "slug": "curriculum/p1/week-05/5-dom-events-talking-to-an-api"
          },
          {
            "slug": "curriculum/p1/week-05/lab"
          }
        ]
      },
      {
        "label": "Week 6 — REST APIs with FastAPI & Pydantic",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-06"
          },
          {
            "slug": "curriculum/p1/week-06/1-rest-design-api-contracts"
          },
          {
            "slug": "curriculum/p1/week-06/2-fastapi-fundamentals"
          },
          {
            "slug": "curriculum/p1/week-06/3-pydantic-v2-validation-as-a-contract"
          },
          {
            "slug": "curriculum/p1/week-06/4-security-auth-hardening"
          },
          {
            "slug": "curriculum/p1/week-06/5-testing-docs-deployment"
          },
          {
            "slug": "curriculum/p1/week-06/lab"
          }
        ]
      },
      {
        "label": "Week 7 — Relational Theory, Modelling & SQL",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-07"
          },
          {
            "slug": "curriculum/p1/week-07/1-relational-model-normalization"
          },
          {
            "slug": "curriculum/p1/week-07/2-er-modelling-schema-design"
          },
          {
            "slug": "curriculum/p1/week-07/3-sql-i-querying"
          },
          {
            "slug": "curriculum/p1/week-07/4-sql-ii-analytical-sql"
          },
          {
            "slug": "curriculum/p1/week-07/5-postgres-in-practice"
          },
          {
            "slug": "curriculum/p1/week-07/lab"
          }
        ]
      },
      {
        "label": "Week 8 — Transactions, Indexing & SQLAlchemy",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-08"
          },
          {
            "slug": "curriculum/p1/week-08/1-transactions-acid-for-real"
          },
          {
            "slug": "curriculum/p1/week-08/2-isolation-levels-concurrency-anomalies"
          },
          {
            "slug": "curriculum/p1/week-08/3-indexing-query-performance"
          },
          {
            "slug": "curriculum/p1/week-08/4-sqlalchemy-2-0-the-orm-boundary"
          },
          {
            "slug": "curriculum/p1/week-08/5-putting-it-together-a-correct-fast-data-layer"
          },
          {
            "slug": "curriculum/p1/week-08/lab"
          }
        ]
      }
    ]
  },
  {
    "label": "Phase 2 · Systems & Data",
    "collapsed": true,
    "items": [
      {
        "label": "Week 9 — Digital Logic → CPU (Nand2Tetris Part I)",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-09"
          },
          {
            "slug": "curriculum/p2/week-09/1-boolean-algebra-logic-gates"
          },
          {
            "slug": "curriculum/p2/week-09/2-combinational-arithmetic"
          },
          {
            "slug": "curriculum/p2/week-09/3-the-alu"
          },
          {
            "slug": "curriculum/p2/week-09/4-sequential-logic-memory-clock"
          },
          {
            "slug": "curriculum/p2/week-09/5-from-cpu-to-program"
          },
          {
            "slug": "curriculum/p2/week-09/lab"
          }
        ]
      },
      {
        "label": "Week 10 — Networking & Raw Sockets",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-10"
          },
          {
            "slug": "curriculum/p2/week-10/1-the-network-stack"
          },
          {
            "slug": "curriculum/p2/week-10/2-tcp-vs-udp"
          },
          {
            "slug": "curriculum/p2/week-10/3-socket-programming"
          },
          {
            "slug": "curriculum/p2/week-10/4-designing-an-application-protocol"
          },
          {
            "slug": "curriculum/p2/week-10/5-network-security-operations-basics"
          },
          {
            "slug": "curriculum/p2/week-10/lab"
          }
        ]
      },
      {
        "label": "Week 11 — Linear Algebra & Calculus for AI",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-11"
          },
          {
            "slug": "curriculum/p2/week-11/0-numpy-in-20-minutes"
          },
          {
            "slug": "curriculum/p2/week-11/1-vectors-vector-spaces"
          },
          {
            "slug": "curriculum/p2/week-11/2-matrices-linear-transformations"
          },
          {
            "slug": "curriculum/p2/week-11/3-eigen-decomposition-svd-pca"
          },
          {
            "slug": "curriculum/p2/week-11/4-calculus-the-chain-rule"
          },
          {
            "slug": "curriculum/p2/week-11/5-optimization"
          },
          {
            "slug": "curriculum/p2/week-11/lab"
          }
        ]
      },
      {
        "label": "Week 12 — Probability, Statistics & Experimentation",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-12"
          },
          {
            "slug": "curriculum/p2/week-12/1-probability-foundations"
          },
          {
            "slug": "curriculum/p2/week-12/2-distributions"
          },
          {
            "slug": "curriculum/p2/week-12/3-statistical-inference"
          },
          {
            "slug": "curriculum/p2/week-12/4-experimentation-a-b-testing"
          },
          {
            "slug": "curriculum/p2/week-12/5-exploratory-statistics-correlation"
          },
          {
            "slug": "curriculum/p2/week-12/lab"
          }
        ]
      },
      {
        "label": "Week 13 — DSA I — Complexity & Linear Structures",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-13"
          },
          {
            "slug": "curriculum/p2/week-13/1-complexity-analysis-properly"
          },
          {
            "slug": "curriculum/p2/week-13/2-arrays-strings-two-pointer-techniques"
          },
          {
            "slug": "curriculum/p2/week-13/3-linked-lists-stacks-queues"
          },
          {
            "slug": "curriculum/p2/week-13/4-hash-tables-from-scratch"
          },
          {
            "slug": "curriculum/p2/week-13/5-sorting-searching-problem-solving-method"
          },
          {
            "slug": "curriculum/p2/week-13/lab"
          }
        ]
      },
      {
        "label": "Week 14 — DSA II — Trees, Graphs & Dynamic Programming",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-14"
          },
          {
            "slug": "curriculum/p2/week-14/1-trees-binary-search-trees"
          },
          {
            "slug": "curriculum/p2/week-14/2-heaps-priority-queues-intervals"
          },
          {
            "slug": "curriculum/p2/week-14/3-graphs-traversal"
          },
          {
            "slug": "curriculum/p2/week-14/4-weighted-shortest-paths-greedy-algorithms"
          },
          {
            "slug": "curriculum/p2/week-14/5-dynamic-programming"
          },
          {
            "slug": "curriculum/p2/week-14/lab"
          }
        ]
      },
      {
        "label": "Week 15 — Data Engineering — Ingestion & Pipelines",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-15"
          },
          {
            "slug": "curriculum/p2/week-15/1-data-engineering-landscape"
          },
          {
            "slug": "curriculum/p2/week-15/2-extracting-from-apis"
          },
          {
            "slug": "curriculum/p2/week-15/3-web-scraping"
          },
          {
            "slug": "curriculum/p2/week-15/4-dlt-declarative-pipelines"
          },
          {
            "slug": "curriculum/p2/week-15/5-storage-warehousing-orchestration"
          },
          {
            "slug": "curriculum/p2/week-15/lab"
          }
        ]
      },
      {
        "label": "Week 16 — Pandas, EDA & Automated Analysis",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-16"
          },
          {
            "slug": "curriculum/p2/week-16/0-scikit-learn-just-enough"
          },
          {
            "slug": "curriculum/p2/week-16/1-numpy-properly"
          },
          {
            "slug": "curriculum/p2/week-16/2-pandas-for-real-work"
          },
          {
            "slug": "curriculum/p2/week-16/3-data-cleaning"
          },
          {
            "slug": "curriculum/p2/week-16/4-exploratory-data-analysis"
          },
          {
            "slug": "curriculum/p2/week-16/5-visualization-that-communicates"
          },
          {
            "slug": "curriculum/p2/week-16/lab"
          }
        ]
      }
    ]
  },
  {
    "label": "Phase 3 · Machine Learning",
    "collapsed": true,
    "items": [
      {
        "label": "Week 17 — Supervised Learning from Scratch",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-17"
          },
          {
            "slug": "curriculum/p3/week-17/1-what-learning-from-data-actually-is"
          },
          {
            "slug": "curriculum/p3/week-17/2-linear-regression-from-mathematical-scratch"
          },
          {
            "slug": "curriculum/p3/week-17/3-logistic-regression-classification"
          },
          {
            "slug": "curriculum/p3/week-17/4-regularization-the-bias-variance-trade-off"
          },
          {
            "slug": "curriculum/p3/week-17/5-scikit-learn-the-industry-surface"
          },
          {
            "slug": "curriculum/p3/week-17/lab"
          }
        ]
      },
      {
        "label": "Week 18 — Trees, Ensembles & Unsupervised Learning",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-18"
          },
          {
            "slug": "curriculum/p3/week-18/1-decision-trees"
          },
          {
            "slug": "curriculum/p3/week-18/2-bagging-random-forests"
          },
          {
            "slug": "curriculum/p3/week-18/3-gradient-boosting-xgboost"
          },
          {
            "slug": "curriculum/p3/week-18/4-unsupervised-learning-clustering"
          },
          {
            "slug": "curriculum/p3/week-18/5-dimensionality-reduction-representation"
          },
          {
            "slug": "curriculum/p3/week-18/lab"
          }
        ]
      },
      {
        "label": "Week 19 — Evaluation, Metrics & Validation",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-19"
          },
          {
            "slug": "curriculum/p3/week-19/1-classification-metrics"
          },
          {
            "slug": "curriculum/p3/week-19/2-regression-ranking-probabilistic-metrics"
          },
          {
            "slug": "curriculum/p3/week-19/3-validation-strategy"
          },
          {
            "slug": "curriculum/p3/week-19/4-data-leakage-the-career-defining-failure-mode"
          },
          {
            "slug": "curriculum/p3/week-19/5-model-selection-error-analysis-reporting"
          },
          {
            "slug": "curriculum/p3/week-19/lab"
          }
        ]
      },
      {
        "label": "Week 20 — Feature Engineering & Imbalanced Data",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-20"
          },
          {
            "slug": "curriculum/p3/week-20/1-numerical-categorical-features"
          },
          {
            "slug": "curriculum/p3/week-20/2-temporal-text-interaction-features"
          },
          {
            "slug": "curriculum/p3/week-20/3-feature-selection-dimensionality"
          },
          {
            "slug": "curriculum/p3/week-20/4-imbalanced-classification"
          },
          {
            "slug": "curriculum/p3/week-20/5-production-feature-pipelines"
          },
          {
            "slug": "curriculum/p3/week-20/lab"
          }
        ]
      },
      {
        "label": "Week 21 — Neural Networks & Backpropagation",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-21"
          },
          {
            "slug": "curriculum/p3/week-21/1-from-linear-models-to-neural-networks"
          },
          {
            "slug": "curriculum/p3/week-21/2-forward-pass-loss-backpropagation"
          },
          {
            "slug": "curriculum/p3/week-21/3-training-dynamics"
          },
          {
            "slug": "curriculum/p3/week-21/4-optimizers-regularization-in-practice"
          },
          {
            "slug": "curriculum/p3/week-21/5-pytorch-fundamentals"
          },
          {
            "slug": "curriculum/p3/week-21/lab"
          }
        ]
      },
      {
        "label": "Week 22 — PyTorch, CNNs & Transfer Learning",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-22"
          },
          {
            "slug": "curriculum/p3/week-22/1-images-as-data-opencv"
          },
          {
            "slug": "curriculum/p3/week-22/2-convolutional-neural-networks"
          },
          {
            "slug": "curriculum/p3/week-22/3-training-a-cnn-properly"
          },
          {
            "slug": "curriculum/p3/week-22/4-transfer-learning"
          },
          {
            "slug": "curriculum/p3/week-22/5-beyond-classification-model-export"
          },
          {
            "slug": "curriculum/p3/week-22/lab"
          }
        ]
      },
      {
        "label": "Week 23 — MLOps I — Packaging, Docker & Serverless",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-23"
          },
          {
            "slug": "curriculum/p3/week-23/1-from-notebook-to-service"
          },
          {
            "slug": "curriculum/p3/week-23/2-serving-with-fastapi"
          },
          {
            "slug": "curriculum/p3/week-23/3-docker"
          },
          {
            "slug": "curriculum/p3/week-23/4-ci-cd"
          },
          {
            "slug": "curriculum/p3/week-23/5-serverless-deployment"
          },
          {
            "slug": "curriculum/p3/week-23/lab"
          }
        ]
      },
      {
        "label": "Week 24 — MLOps II — Kubernetes & Model Serving",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-24"
          },
          {
            "slug": "curriculum/p3/week-24/1-why-orchestration-exists"
          },
          {
            "slug": "curriculum/p3/week-24/2-deployments-services-configuration"
          },
          {
            "slug": "curriculum/p3/week-24/3-resources-scheduling-autoscaling"
          },
          {
            "slug": "curriculum/p3/week-24/4-model-serving-frameworks"
          },
          {
            "slug": "curriculum/p3/week-24/5-operating-an-ml-service"
          },
          {
            "slug": "curriculum/p3/week-24/lab"
          }
        ]
      }
    ]
  },
  {
    "label": "Phase 4 · Generative AI",
    "collapsed": true,
    "items": [
      {
        "label": "Week 25 — Tokenizers & Transformer Internals",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-25"
          },
          {
            "slug": "curriculum/p4/week-25/1-text-tokens"
          },
          {
            "slug": "curriculum/p4/week-25/2-embeddings-positional-information"
          },
          {
            "slug": "curriculum/p4/week-25/3-self-attention"
          },
          {
            "slug": "curriculum/p4/week-25/4-the-transformer-block-the-full-decoder"
          },
          {
            "slug": "curriculum/p4/week-25/5-generation-decoding-inference-cost"
          },
          {
            "slug": "curriculum/p4/week-25/6-reasoning-effort-and-thinking-budgets"
          },
          {
            "slug": "curriculum/p4/week-25/lab"
          }
        ]
      },
      {
        "label": "Week 26 — Quantization, PEFT & Local Serving",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-26"
          },
          {
            "slug": "curriculum/p4/week-26/1-numeric-precision-quantization"
          },
          {
            "slug": "curriculum/p4/week-26/2-fine-tuning-when-and-why"
          },
          {
            "slug": "curriculum/p4/week-26/3-lora-qlora"
          },
          {
            "slug": "curriculum/p4/week-26/4-structured-output-tool-calling-behaviour"
          },
          {
            "slug": "curriculum/p4/week-26/5-local-self-hosted-serving"
          },
          {
            "slug": "curriculum/p4/week-26/lab"
          }
        ]
      },
      {
        "label": "Week 27 — RAG I — Chunking, Embeddings & Vector Indexes",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-27"
          },
          {
            "slug": "curriculum/p4/week-27/1-why-rag-and-the-ingestion-problem"
          },
          {
            "slug": "curriculum/p4/week-27/2-chunking-strategies"
          },
          {
            "slug": "curriculum/p4/week-27/3-embeddings-for-retrieval"
          },
          {
            "slug": "curriculum/p4/week-27/4-vector-indexes-flat-ivf-hnsw"
          },
          {
            "slug": "curriculum/p4/week-27/5-building-evaluating-a-retrieval-system"
          },
          {
            "slug": "curriculum/p4/week-27/lab"
          }
        ]
      },
      {
        "label": "Week 28 — RAG II — Hybrid Search, Re-ranking & Caching",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-28"
          },
          {
            "slug": "curriculum/p4/week-28/1-sparse-retrieval-bm25"
          },
          {
            "slug": "curriculum/p4/week-28/2-hybrid-search-fusion"
          },
          {
            "slug": "curriculum/p4/week-28/3-query-understanding-transformation"
          },
          {
            "slug": "curriculum/p4/week-28/4-re-ranking-with-cross-encoders"
          },
          {
            "slug": "curriculum/p4/week-28/5-caching-cost-production-rag-operations"
          },
          {
            "slug": "curriculum/p4/week-28/lab"
          }
        ]
      },
      {
        "label": "Week 29 — Agents I — Loops, Tools & MCP",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-29"
          },
          {
            "slug": "curriculum/p4/week-29/1-what-an-agent-actually-is"
          },
          {
            "slug": "curriculum/p4/week-29/2-tools-function-calling"
          },
          {
            "slug": "curriculum/p4/week-29/3-memory-context-state"
          },
          {
            "slug": "curriculum/p4/week-29/4-model-context-protocol-mcp"
          },
          {
            "slug": "curriculum/p4/week-29/5-pydantic-ai-typed-agents"
          },
          {
            "slug": "curriculum/p4/week-29/lab"
          }
        ]
      },
      {
        "label": "Week 30 — Agents II — LangGraph, Multi-Agent & Durability",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-30"
          },
          {
            "slug": "curriculum/p4/week-30/1-graphs-as-the-right-abstraction"
          },
          {
            "slug": "curriculum/p4/week-30/2-multi-agent-patterns"
          },
          {
            "slug": "curriculum/p4/week-30/3-durable-execution-checkpoint-resume"
          },
          {
            "slug": "curriculum/p4/week-30/4-resilience-budgets-failure-handling"
          },
          {
            "slug": "curriculum/p4/week-30/5-architecting-a-real-agentic-system"
          },
          {
            "slug": "curriculum/p4/week-30/lab"
          }
        ]
      },
      {
        "label": "Week 31 — Evals & Defensive AI",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-31"
          },
          {
            "slug": "curriculum/p4/week-31/1-why-evals-and-how-to-build-a-dataset"
          },
          {
            "slug": "curriculum/p4/week-31/2-llm-as-a-judge"
          },
          {
            "slug": "curriculum/p4/week-31/3-rag-agent-specific-evaluation"
          },
          {
            "slug": "curriculum/p4/week-31/4-prompt-injection-defensive-design"
          },
          {
            "slug": "curriculum/p4/week-31/5-guardrails-moderation"
          },
          {
            "slug": "curriculum/p4/week-31/lab"
          }
        ]
      },
      {
        "label": "Week 32 — LLMOps — Observability, Cost & Reliability",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-32"
          },
          {
            "slug": "curriculum/p4/week-32/1-tracing-opentelemetry"
          },
          {
            "slug": "curriculum/p4/week-32/2-langfuse-the-llm-observability-stack"
          },
          {
            "slug": "curriculum/p4/week-32/3-cost-engineering"
          },
          {
            "slug": "curriculum/p4/week-32/4-reliability-latency-production-operations"
          },
          {
            "slug": "curriculum/p4/week-32/5-deploying-maintaining-an-ai-system"
          },
          {
            "slug": "curriculum/p4/week-32/lab"
          }
        ]
      }
    ]
  },
  {
    "label": "Labs",
    "collapsed": true,
    "items": [
      {
        "label": "Setup",
        "collapsed": true,
        "items": [
          {
            "slug": "labs"
          },
          {
            "slug": "labs/verify"
          }
        ]
      },
      {
        "label": "Week 1",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-01/lab"
          }
        ]
      },
      {
        "label": "Week 2",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-02/lab"
          }
        ]
      },
      {
        "label": "Week 3",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-03/lab"
          }
        ]
      },
      {
        "label": "Week 4",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-04/lab"
          }
        ]
      },
      {
        "label": "Week 5",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-05/lab"
          }
        ]
      },
      {
        "label": "Week 6",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-06/lab"
          }
        ]
      },
      {
        "label": "Week 7",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-07/lab"
          }
        ]
      },
      {
        "label": "Week 8",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p1/week-08/lab"
          }
        ]
      },
      {
        "label": "Week 9",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-09/lab"
          }
        ]
      },
      {
        "label": "Week 10",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-10/lab"
          }
        ]
      },
      {
        "label": "Week 11",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-11/lab"
          }
        ]
      },
      {
        "label": "Week 12",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-12/lab"
          }
        ]
      },
      {
        "label": "Week 13",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-13/lab"
          }
        ]
      },
      {
        "label": "Week 14",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-14/lab"
          }
        ]
      },
      {
        "label": "Week 15",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-15/lab"
          }
        ]
      },
      {
        "label": "Week 16",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p2/week-16/lab"
          }
        ]
      },
      {
        "label": "Week 17",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-17/lab"
          }
        ]
      },
      {
        "label": "Week 18",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-18/lab"
          }
        ]
      },
      {
        "label": "Week 19",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-19/lab"
          }
        ]
      },
      {
        "label": "Week 20",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-20/lab"
          }
        ]
      },
      {
        "label": "Week 21",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-21/lab"
          }
        ]
      },
      {
        "label": "Week 22",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-22/lab"
          }
        ]
      },
      {
        "label": "Week 23",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-23/lab"
          }
        ]
      },
      {
        "label": "Week 24",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p3/week-24/lab"
          }
        ]
      },
      {
        "label": "Week 25",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-25/lab"
          }
        ]
      },
      {
        "label": "Week 26",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-26/lab"
          }
        ]
      },
      {
        "label": "Week 27",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-27/lab"
          }
        ]
      },
      {
        "label": "Week 28",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-28/lab"
          }
        ]
      },
      {
        "label": "Week 29",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-29/lab"
          }
        ]
      },
      {
        "label": "Week 30",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-30/lab"
          }
        ]
      },
      {
        "label": "Week 31",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-31/lab"
          }
        ]
      },
      {
        "label": "Week 32",
        "collapsed": true,
        "items": [
          {
            "slug": "curriculum/p4/week-32/lab"
          }
        ]
      }
    ]
  },
  {
    "label": "Projects",
    "collapsed": true,
    "items": [
      {
        "label": "Portfolio gates",
        "collapsed": true,
        "items": [
          {
            "slug": "projects/midterm"
          },
          {
            "slug": "projects/capstone"
          },
          {
            "slug": "projects/defence"
          }
        ]
      }
    ]
  },
  {
    "label": "Reference",
    "collapsed": true,
    "items": [
      {
        "label": "Library",
        "collapsed": true,
        "items": [
          {
            "slug": "reference/papers"
          },
          {
            "slug": "reference/tools"
          },
          {
            "slug": "reference/glossary"
          },
          {
            "slug": "reference/diagram-index"
          },
          {
            "slug": "reference/cheatsheets"
          }
        ]
      }
    ]
  },
  {
    "label": "Solutions",
    "collapsed": true,
    "items": [
      {
        "label": "How to use these",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions"
          }
        ]
      },
      {
        "label": "Week 1",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p1/week-01/p1-w01-m1"
          },
          {
            "slug": "solutions/p1/week-01/p1-w01-m2"
          },
          {
            "slug": "solutions/p1/week-01/p1-w01-m3"
          },
          {
            "slug": "solutions/p1/week-01/p1-w01-m4"
          },
          {
            "slug": "solutions/p1/week-01/p1-w01-m5"
          },
          {
            "slug": "solutions/p1/week-01/lab"
          }
        ]
      },
      {
        "label": "Week 2",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p1/week-02/p1-w02-m1"
          },
          {
            "slug": "solutions/p1/week-02/p1-w02-m2"
          },
          {
            "slug": "solutions/p1/week-02/p1-w02-m3"
          },
          {
            "slug": "solutions/p1/week-02/p1-w02-m4"
          },
          {
            "slug": "solutions/p1/week-02/p1-w02-m5"
          },
          {
            "slug": "solutions/p1/week-02/lab"
          }
        ]
      },
      {
        "label": "Week 3",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p1/week-03/p1-w03-m1"
          },
          {
            "slug": "solutions/p1/week-03/p1-w03-m2"
          },
          {
            "slug": "solutions/p1/week-03/p1-w03-m3"
          },
          {
            "slug": "solutions/p1/week-03/p1-w03-m4"
          },
          {
            "slug": "solutions/p1/week-03/p1-w03-m5"
          },
          {
            "slug": "solutions/p1/week-03/lab"
          }
        ]
      },
      {
        "label": "Week 4",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p1/week-04/p1-w04-m1"
          },
          {
            "slug": "solutions/p1/week-04/p1-w04-m2"
          },
          {
            "slug": "solutions/p1/week-04/p1-w04-m3"
          },
          {
            "slug": "solutions/p1/week-04/p1-w04-m4"
          },
          {
            "slug": "solutions/p1/week-04/p1-w04-m5"
          },
          {
            "slug": "solutions/p1/week-04/lab"
          }
        ]
      },
      {
        "label": "Week 5",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p1/week-05/p1-w05-m1"
          },
          {
            "slug": "solutions/p1/week-05/p1-w05-m2"
          },
          {
            "slug": "solutions/p1/week-05/p1-w05-m3"
          },
          {
            "slug": "solutions/p1/week-05/p1-w05-m4"
          },
          {
            "slug": "solutions/p1/week-05/p1-w05-m5"
          },
          {
            "slug": "solutions/p1/week-05/lab"
          }
        ]
      },
      {
        "label": "Week 6",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p1/week-06/p1-w06-m1"
          },
          {
            "slug": "solutions/p1/week-06/p1-w06-m2"
          },
          {
            "slug": "solutions/p1/week-06/p1-w06-m3"
          },
          {
            "slug": "solutions/p1/week-06/p1-w06-m4"
          },
          {
            "slug": "solutions/p1/week-06/p1-w06-m5"
          },
          {
            "slug": "solutions/p1/week-06/lab"
          }
        ]
      },
      {
        "label": "Week 7",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p1/week-07/p1-w07-m1"
          },
          {
            "slug": "solutions/p1/week-07/p1-w07-m2"
          },
          {
            "slug": "solutions/p1/week-07/p1-w07-m3"
          },
          {
            "slug": "solutions/p1/week-07/p1-w07-m4"
          },
          {
            "slug": "solutions/p1/week-07/p1-w07-m5"
          },
          {
            "slug": "solutions/p1/week-07/lab"
          }
        ]
      },
      {
        "label": "Week 8",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p1/week-08/p1-w08-m1"
          },
          {
            "slug": "solutions/p1/week-08/p1-w08-m2"
          },
          {
            "slug": "solutions/p1/week-08/p1-w08-m3"
          },
          {
            "slug": "solutions/p1/week-08/p1-w08-m4"
          },
          {
            "slug": "solutions/p1/week-08/p1-w08-m5"
          },
          {
            "slug": "solutions/p1/week-08/lab"
          }
        ]
      },
      {
        "label": "Week 9",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p2/week-09/p2-w09-m1"
          },
          {
            "slug": "solutions/p2/week-09/p2-w09-m2"
          },
          {
            "slug": "solutions/p2/week-09/p2-w09-m3"
          },
          {
            "slug": "solutions/p2/week-09/p2-w09-m4"
          },
          {
            "slug": "solutions/p2/week-09/p2-w09-m5"
          },
          {
            "slug": "solutions/p2/week-09/lab"
          }
        ]
      },
      {
        "label": "Week 10",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p2/week-10/p2-w10-m1"
          },
          {
            "slug": "solutions/p2/week-10/p2-w10-m2"
          },
          {
            "slug": "solutions/p2/week-10/p2-w10-m3"
          },
          {
            "slug": "solutions/p2/week-10/p2-w10-m4"
          },
          {
            "slug": "solutions/p2/week-10/p2-w10-m5"
          },
          {
            "slug": "solutions/p2/week-10/lab"
          }
        ]
      },
      {
        "label": "Week 11",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p2/week-11/p2-w11-m1"
          },
          {
            "slug": "solutions/p2/week-11/p2-w11-m2"
          },
          {
            "slug": "solutions/p2/week-11/p2-w11-m3"
          },
          {
            "slug": "solutions/p2/week-11/p2-w11-m4"
          },
          {
            "slug": "solutions/p2/week-11/p2-w11-m5"
          },
          {
            "slug": "solutions/p2/week-11/lab"
          }
        ]
      },
      {
        "label": "Week 12",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p2/week-12/p2-w12-m1"
          },
          {
            "slug": "solutions/p2/week-12/p2-w12-m2"
          },
          {
            "slug": "solutions/p2/week-12/p2-w12-m3"
          },
          {
            "slug": "solutions/p2/week-12/p2-w12-m4"
          },
          {
            "slug": "solutions/p2/week-12/p2-w12-m5"
          },
          {
            "slug": "solutions/p2/week-12/lab"
          }
        ]
      },
      {
        "label": "Week 13",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p2/week-13/p2-w13-m1"
          },
          {
            "slug": "solutions/p2/week-13/p2-w13-m2"
          },
          {
            "slug": "solutions/p2/week-13/p2-w13-m3"
          },
          {
            "slug": "solutions/p2/week-13/p2-w13-m4"
          },
          {
            "slug": "solutions/p2/week-13/p2-w13-m5"
          },
          {
            "slug": "solutions/p2/week-13/lab"
          }
        ]
      },
      {
        "label": "Week 14",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p2/week-14/p2-w14-m1"
          },
          {
            "slug": "solutions/p2/week-14/p2-w14-m2"
          },
          {
            "slug": "solutions/p2/week-14/p2-w14-m3"
          },
          {
            "slug": "solutions/p2/week-14/p2-w14-m4"
          },
          {
            "slug": "solutions/p2/week-14/p2-w14-m5"
          },
          {
            "slug": "solutions/p2/week-14/lab"
          }
        ]
      },
      {
        "label": "Week 15",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p2/week-15/p2-w15-m1"
          },
          {
            "slug": "solutions/p2/week-15/p2-w15-m2"
          },
          {
            "slug": "solutions/p2/week-15/p2-w15-m3"
          },
          {
            "slug": "solutions/p2/week-15/p2-w15-m4"
          },
          {
            "slug": "solutions/p2/week-15/p2-w15-m5"
          },
          {
            "slug": "solutions/p2/week-15/lab"
          }
        ]
      },
      {
        "label": "Week 16",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p2/week-16/p2-w16-m1"
          },
          {
            "slug": "solutions/p2/week-16/p2-w16-m2"
          },
          {
            "slug": "solutions/p2/week-16/p2-w16-m3"
          },
          {
            "slug": "solutions/p2/week-16/p2-w16-m4"
          },
          {
            "slug": "solutions/p2/week-16/p2-w16-m5"
          },
          {
            "slug": "solutions/p2/week-16/lab"
          }
        ]
      },
      {
        "label": "Week 17",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p3/week-17/p3-w17-m1"
          },
          {
            "slug": "solutions/p3/week-17/p3-w17-m2"
          },
          {
            "slug": "solutions/p3/week-17/p3-w17-m3"
          },
          {
            "slug": "solutions/p3/week-17/p3-w17-m4"
          },
          {
            "slug": "solutions/p3/week-17/p3-w17-m5"
          },
          {
            "slug": "solutions/p3/week-17/lab"
          }
        ]
      },
      {
        "label": "Week 18",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p3/week-18/p3-w18-m1"
          },
          {
            "slug": "solutions/p3/week-18/p3-w18-m2"
          },
          {
            "slug": "solutions/p3/week-18/p3-w18-m3"
          },
          {
            "slug": "solutions/p3/week-18/p3-w18-m4"
          },
          {
            "slug": "solutions/p3/week-18/p3-w18-m5"
          },
          {
            "slug": "solutions/p3/week-18/lab"
          }
        ]
      },
      {
        "label": "Week 19",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p3/week-19/p3-w19-m1"
          },
          {
            "slug": "solutions/p3/week-19/p3-w19-m2"
          },
          {
            "slug": "solutions/p3/week-19/p3-w19-m3"
          },
          {
            "slug": "solutions/p3/week-19/p3-w19-m4"
          },
          {
            "slug": "solutions/p3/week-19/p3-w19-m5"
          },
          {
            "slug": "solutions/p3/week-19/lab"
          }
        ]
      },
      {
        "label": "Week 20",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p3/week-20/p3-w20-m1"
          },
          {
            "slug": "solutions/p3/week-20/p3-w20-m2"
          },
          {
            "slug": "solutions/p3/week-20/p3-w20-m3"
          },
          {
            "slug": "solutions/p3/week-20/p3-w20-m4"
          },
          {
            "slug": "solutions/p3/week-20/p3-w20-m5"
          },
          {
            "slug": "solutions/p3/week-20/lab"
          }
        ]
      },
      {
        "label": "Week 21",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p3/week-21/p3-w21-m1"
          },
          {
            "slug": "solutions/p3/week-21/p3-w21-m2"
          },
          {
            "slug": "solutions/p3/week-21/p3-w21-m3"
          },
          {
            "slug": "solutions/p3/week-21/p3-w21-m4"
          },
          {
            "slug": "solutions/p3/week-21/p3-w21-m5"
          },
          {
            "slug": "solutions/p3/week-21/lab"
          }
        ]
      },
      {
        "label": "Week 22",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p3/week-22/p3-w22-m1"
          },
          {
            "slug": "solutions/p3/week-22/p3-w22-m2"
          },
          {
            "slug": "solutions/p3/week-22/p3-w22-m3"
          },
          {
            "slug": "solutions/p3/week-22/p3-w22-m4"
          },
          {
            "slug": "solutions/p3/week-22/p3-w22-m5"
          },
          {
            "slug": "solutions/p3/week-22/lab"
          }
        ]
      },
      {
        "label": "Week 23",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p3/week-23/p3-w23-m1"
          },
          {
            "slug": "solutions/p3/week-23/p3-w23-m2"
          },
          {
            "slug": "solutions/p3/week-23/p3-w23-m3"
          },
          {
            "slug": "solutions/p3/week-23/p3-w23-m4"
          },
          {
            "slug": "solutions/p3/week-23/p3-w23-m5"
          },
          {
            "slug": "solutions/p3/week-23/lab"
          }
        ]
      },
      {
        "label": "Week 24",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p3/week-24/p3-w24-m1"
          },
          {
            "slug": "solutions/p3/week-24/p3-w24-m2"
          },
          {
            "slug": "solutions/p3/week-24/p3-w24-m3"
          },
          {
            "slug": "solutions/p3/week-24/p3-w24-m4"
          },
          {
            "slug": "solutions/p3/week-24/p3-w24-m5"
          },
          {
            "slug": "solutions/p3/week-24/lab"
          }
        ]
      },
      {
        "label": "Week 25",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p4/week-25/p4-w25-m1"
          },
          {
            "slug": "solutions/p4/week-25/p4-w25-m2"
          },
          {
            "slug": "solutions/p4/week-25/p4-w25-m3"
          },
          {
            "slug": "solutions/p4/week-25/p4-w25-m4"
          },
          {
            "slug": "solutions/p4/week-25/p4-w25-m5"
          },
          {
            "slug": "solutions/p4/week-25/lab"
          }
        ]
      },
      {
        "label": "Week 26",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p4/week-26/p4-w26-m1"
          },
          {
            "slug": "solutions/p4/week-26/p4-w26-m2"
          },
          {
            "slug": "solutions/p4/week-26/p4-w26-m3"
          },
          {
            "slug": "solutions/p4/week-26/p4-w26-m4"
          },
          {
            "slug": "solutions/p4/week-26/p4-w26-m5"
          },
          {
            "slug": "solutions/p4/week-26/lab"
          }
        ]
      },
      {
        "label": "Week 27",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p4/week-27/p4-w27-m1"
          },
          {
            "slug": "solutions/p4/week-27/p4-w27-m2"
          },
          {
            "slug": "solutions/p4/week-27/p4-w27-m3"
          },
          {
            "slug": "solutions/p4/week-27/p4-w27-m4"
          },
          {
            "slug": "solutions/p4/week-27/p4-w27-m5"
          },
          {
            "slug": "solutions/p4/week-27/lab"
          }
        ]
      },
      {
        "label": "Week 28",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p4/week-28/p4-w28-m1"
          },
          {
            "slug": "solutions/p4/week-28/p4-w28-m2"
          },
          {
            "slug": "solutions/p4/week-28/p4-w28-m3"
          },
          {
            "slug": "solutions/p4/week-28/p4-w28-m4"
          },
          {
            "slug": "solutions/p4/week-28/p4-w28-m5"
          },
          {
            "slug": "solutions/p4/week-28/lab"
          }
        ]
      },
      {
        "label": "Week 29",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p4/week-29/p4-w29-m1"
          },
          {
            "slug": "solutions/p4/week-29/p4-w29-m2"
          },
          {
            "slug": "solutions/p4/week-29/p4-w29-m3"
          },
          {
            "slug": "solutions/p4/week-29/p4-w29-m4"
          },
          {
            "slug": "solutions/p4/week-29/p4-w29-m5"
          },
          {
            "slug": "solutions/p4/week-29/lab"
          }
        ]
      },
      {
        "label": "Week 30",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p4/week-30/p4-w30-m1"
          },
          {
            "slug": "solutions/p4/week-30/p4-w30-m2"
          },
          {
            "slug": "solutions/p4/week-30/p4-w30-m3"
          },
          {
            "slug": "solutions/p4/week-30/p4-w30-m4"
          },
          {
            "slug": "solutions/p4/week-30/p4-w30-m5"
          },
          {
            "slug": "solutions/p4/week-30/lab"
          }
        ]
      },
      {
        "label": "Week 31",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p4/week-31/p4-w31-m1"
          },
          {
            "slug": "solutions/p4/week-31/p4-w31-m2"
          },
          {
            "slug": "solutions/p4/week-31/p4-w31-m3"
          },
          {
            "slug": "solutions/p4/week-31/p4-w31-m4"
          },
          {
            "slug": "solutions/p4/week-31/p4-w31-m5"
          },
          {
            "slug": "solutions/p4/week-31/lab"
          }
        ]
      },
      {
        "label": "Week 32",
        "collapsed": true,
        "items": [
          {
            "slug": "solutions/p4/week-32/p4-w32-m1"
          },
          {
            "slug": "solutions/p4/week-32/p4-w32-m2"
          },
          {
            "slug": "solutions/p4/week-32/p4-w32-m3"
          },
          {
            "slug": "solutions/p4/week-32/p4-w32-m4"
          },
          {
            "slug": "solutions/p4/week-32/p4-w32-m5"
          },
          {
            "slug": "solutions/p4/week-32/lab"
          }
        ]
      }
    ]
  },
  {
    "label": "Instructor",
    "collapsed": true,
    "items": [
      {
        "label": "Teaching",
        "collapsed": true,
        "items": [
          {
            "slug": "instructor"
          },
          {
            "slug": "instructor/session-plans"
          },
          {
            "slug": "instructor/rubrics"
          },
          {
            "slug": "instructor/release-schedule"
          },
          {
            "slug": "instructor/common-questions"
          }
        ]
      }
    ]
  }
];

export default defineConfig({
  site: 'https://example.github.io',
  base: '/',
  integrations: [starlight({
    title: 'Nexus',
    description: 'Systems, Machine Learning & Distributed AI — 0 to expert in 32 weeks.',
    customCss: ['./src/styles/nexus.css'],
    components: {
      Header: './src/components/Header.astro',
      PageTitle: './src/components/PageTitle.astro',
    },
    sidebar,
    pagination: true,
    lastUpdated: false,
    tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
  })],
});
