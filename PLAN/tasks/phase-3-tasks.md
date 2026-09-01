# Phase 3 — Granular Task Breakdown (Weeks 17–24)
**Goal:** train models you understand mathematically, evaluate them so you can defend the number, and deploy them like a production service.

---

## T-P3-W17 — Week 17: Supervised Learning from Scratch

**Week outcome:** learner derives, implements and trains linear/logistic regression without a library, then reproduces it in scikit-learn and knows what the library was doing.

### `P3-W17-M1` — What learning from data actually is
- Micro-lessons: (a) supervised vs unsupervised vs reinforcement; (b) features, labels, samples; (c) hypothesis, parameters, loss; (d) training vs inference; (e) the train/val/test split; (f) generalization
- **L1 Ground:** predict house price from size with a hand-drawn line; adjust it until the error shrinks. That *is* training.
- **L2 Build:** the ML problem-framing checklist (what is the unit of prediction? what's the label? when is it available? what decision does it drive?), baseline-first discipline.
- **L3 Edge:** why a model is a compression of data, the no-free-lunch theorem in plain terms, and the single biggest cause of failed ML projects: the wrong problem framing. Three real post-mortems.
- **Hands-on:** frame 5 messy business requests into precise ML problems (or reject them as not-ML) with written justification.

### `P3-W17-M2` — Linear regression from mathematical scratch
- Micro-lessons: (a) the model; (b) MSE loss; (c) gradient derivation; (d) gradient descent implementation; (e) the normal equation; (f) feature scaling
- **L1 Ground:** one feature, one weight, one bias — code the update rule in 15 lines and watch the loss drop.
- **L2 Build:** vectorized multi-feature implementation, closed form vs GD (and when each is right), scaling's effect on convergence, R² and residual analysis, polynomial features.
- **L3 Edge:** normal equation cost O(d³) and conditioning; ridge as a fix for singular X'X, derived; SGD vs batch on 10M rows measured; connection to the linear layer in a neural net (Week 21) — same math.
- **Hands-on:** implement both solvers; find the dataset size where GD beats the normal equation; plot the crossover.

### `P3-W17-M3` — Logistic regression & classification
- Micro-lessons: (a) from regression to classification; (b) sigmoid & odds; (c) cross-entropy loss and why not MSE; (d) gradient derivation; (e) decision boundary & threshold; (f) multiclass via softmax
- **L1 Ground:** classify pass/fail from study hours; plot the S-curve and the boundary.
- **L2 Build:** full NumPy implementation with regularization, probability calibration intuition, threshold as a *business* decision not a default 0.5, one-vs-rest vs softmax.
- **L3 Edge:** convexity of the log-loss (and why MSE + sigmoid is non-convex — show it), maximum likelihood derivation, calibration curves and Platt scaling, class weights vs resampling.
- **Hands-on:** derive the gradient on paper, implement it, and verify against a numerical gradient to 1e-7.

### `P3-W17-M4` — Regularization & the bias-variance trade-off
- Micro-lessons: (a) underfitting vs overfitting; (b) bias-variance decomposition; (c) L1/Lasso & L2/Ridge; (d) elastic net; (e) learning curves; (f) model capacity
- **L1 Ground:** fit polynomials of degree 1/4/15 to the same 20 points and look at what happens.
- **L2 Build:** choosing λ by validation, L1's feature-selection property demonstrated, reading learning curves to decide "more data" vs "more capacity", early stopping.
- **L3 Edge:** the geometry of why L1 gives sparsity (with the diamond/circle picture and a proof sketch); double descent in modern over-parameterized models; regularization as a prior (Bayesian view) — this reframes weight decay in Week 26 fine-tuning.
- **Hands-on:** reproduce a double-descent curve and explain why the classical U-shape story is incomplete.

### `P3-W17-M5` — scikit-learn: the industry surface
- Micro-lessons: (a) estimator API (`fit`/`predict`/`transform`); (b) `Pipeline`; (c) `ColumnTransformer`; (d) train/test split correctness; (e) `GridSearchCV`; (f) persistence
- **L1 Ground:** the same problem you hand-coded, in 6 lines of scikit-learn — and a diff of the results.
- **L2 Build:** pipelines that prevent leakage by construction, custom transformers via `BaseEstimator`/`TransformerMixin`, `set_output` for DataFrames, reproducibility with `random_state`.
- **L3 Edge:** reading scikit-learn source for `LogisticRegression` (solvers: lbfgs/liblinear/saga and when each matters), why your from-scratch result differs slightly, memory/CPU behaviour with `n_jobs`.
- **Hands-on:** write a custom transformer and drop it into a `Pipeline` inside `GridSearchCV` without leakage.

### `LAB-P3-W17` — **`scratchml`: regression & classification from NumPy**
- `basic`: single-feature linear regression with GD, tests provided.
- `standard`: `LinearRegression` and `LogisticRegression` classes with scikit-learn-compatible API — vectorized, regularized, with GD/SGD/mini-batch, convergence tracking, gradient checks, and results matching scikit-learn within tolerance on 3 datasets.
- `hard`: add softmax multiclass + early stopping + a learning-curve diagnostic tool; train on 1M rows within a memory budget.
- **Ship it:** repo + a blog-style derivation write-up (excellent interview and LinkedIn artifact).

---

## T-P3-W18 — Week 18: Trees, Ensembles & Unsupervised Learning

**Week outcome:** learner can win most tabular problems with gradient boosting and knows why it wins; can segment data without labels.

### `P3-W18-M1` — Decision trees
- Micro-lessons: (a) splits & impurity (Gini/entropy); (b) growing a tree; (c) regression trees; (d) pruning & depth control; (e) interpretability; (f) instability
- **L1 Ground:** build a 3-level tree by hand on 12 rows; compute one Gini split yourself.
- **L2 Build:** implement a decision tree from scratch; hyperparameters that actually matter (`max_depth`, `min_samples_leaf`); why trees need no scaling; extracting rules for stakeholders.
- **L3 Edge:** greedy splitting is not optimal (NP-hard); high variance demonstrated by perturbing one row; axis-aligned split limitations; missing-value handling strategies compared.
- **Hands-on:** implement CART from scratch and match scikit-learn's predictions on a small dataset.

### `P3-W18-M2` — Bagging & random forests
- Micro-lessons: (a) bootstrap; (b) bagging variance reduction; (c) random feature subsets; (d) OOB estimation; (e) feature importance; (f) hyperparameters
- **L1 Ground:** train 1 tree vs 100 trees; compare accuracy and stability.
- **L2 Build:** tuning forests, OOB as free validation, impurity importance vs permutation importance (and why impurity importance lies with high-cardinality features), parallelism.
- **L3 Edge:** the variance-reduction math (correlation between trees caps the benefit), extremely randomized trees, forests on high-dimensional sparse data (and why they lose to linear models there), memory footprint of 500 deep trees.
- **Hands-on:** demonstrate the feature-importance trap: inject a random high-cardinality ID column and show it ranking first under impurity importance.

### `P3-W18-M3` — Gradient boosting & XGBoost
- Micro-lessons: (a) boosting intuition (fit the residuals); (b) gradient boosting derivation; (c) XGBoost's objective & regularization; (d) key hyperparameters; (e) early stopping; (f) LightGBM/CatBoost differences
- **L1 Ground:** three sequential stumps correcting each other, by hand.
- **L2 Build:** full XGBoost workflow — `DMatrix`/sklearn API, `learning_rate` × `n_estimators` trade-off, `max_depth`/`subsample`/`colsample`, `scale_pos_weight`, early stopping on a validation set, categorical handling.
- **L3 Edge:** second-order (Newton) approximation in the XGBoost objective derived; histogram-based splitting and why LightGBM is faster; GOSS/EFB; leaf-wise vs level-wise growth; SHAP values for boosted trees; why GBDTs still beat deep nets on tabular data (cite the benchmarks).
- **Hands-on:** hyperparameter study — 30 configurations, report the sensitivity ranking, and defend a default recipe.

### `P3-W18-M4` — Unsupervised learning: clustering
- Micro-lessons: (a) what "no labels" changes; (b) K-Means & Lloyd's algorithm; (c) choosing k (elbow, silhouette); (d) hierarchical clustering; (e) DBSCAN; (f) evaluating clusters
- **L1 Ground:** run K-Means on 2-D points and watch the centroids move.
- **L2 Build:** implement K-Means from scratch, scaling requirements, k-means++ init, when DBSCAN beats K-Means (non-spherical, noise), interpreting clusters into a business segmentation.
- **L3 Edge:** K-Means as EM with hard assignments; its failure on anisotropic/unequal-variance clusters (demonstrated); clustering at 10M points (mini-batch K-Means, FAISS) — the same machinery as vector-index clustering (IVF) in Week 27.
- **Hands-on:** cluster customers, then produce a one-page segment description a marketing team could act on.

### `P3-W18-M5` — Dimensionality reduction & representation
- Micro-lessons: (a) why reduce dimensions; (b) PCA revisited as an ML tool; (c) t-SNE; (d) UMAP; (e) reading embedding plots honestly; (f) reduction inside a pipeline
- **L1 Ground:** PCA a 30-feature dataset to 2-D and plot the classes.
- **L2 Build:** PCA for speed/denoising, choosing components by explained variance, t-SNE/UMAP for *visualization only*, perplexity/n_neighbors effects, fitting the reducer on train only.
- **L3 Edge:** t-SNE's distortions — cluster sizes and inter-cluster distances are not meaningful (demonstrated with a constructed counterexample); UMAP's topological basis; visualizing 10k text embeddings and the misreadings to avoid (used in Week 27 to inspect retrieval quality).
- **Hands-on:** produce a t-SNE plot and then write the three claims a reader would wrongly make from it, with the correct check for each.

### `LAB-P3-W18` — **Customer churn: end-to-end tabular modelling**
- `basic`: train a random forest on a prepared dataset; report accuracy.
- `standard`: full workflow on a real churn dataset — baseline → logistic regression → random forest → XGBoost, proper validation, hyperparameter search, feature importance with permutation, calibration check, and a business-facing recommendation with an estimated £/$ impact; plus K-Means segmentation of the churners.
- `hard`: beat a stated AUC target under a training-time budget; add SHAP explanations for 5 individual customers; write the model card.
- **Ship it:** repo + model card + a stakeholder one-pager. Directly reusable at work.

---

## T-P3-W19 — Week 19: Evaluation, Metrics & Validation

**Week outcome:** learner can prove a model works — and, more valuably, detect when a good-looking number is a lie.

### `P3-W19-M1` — Classification metrics
- Micro-lessons: (a) confusion matrix; (b) accuracy and its failure; (c) precision, recall, specificity; (d) F1 and Fβ; (e) ROC-AUC; (f) PR-AUC; (g) multiclass averaging
- **L1 Ground:** build a confusion matrix by hand for 20 predictions; compute every metric from it.
- **L2 Build:** metric selection driven by the cost of each error type, ROC vs PR under imbalance (with the same model plotted both ways), macro vs micro vs weighted averaging, per-class breakdowns.
- **L3 Edge:** why ROC-AUC is over-optimistic at 0.1% prevalence (worked numerically); AUC as probability of correct ranking; when a single number is the wrong deliverable; metric gaming.
- **Hands-on:** given a business scenario with stated costs of FP and FN, derive the optimal threshold and the expected cost.

### `P3-W19-M2` — Regression, ranking & probabilistic metrics
- Micro-lessons: (a) MAE/MSE/RMSE; (b) MAPE & its traps; (c) R² and adjusted R²; (d) quantile loss; (e) ranking metrics (NDCG, MRR, Recall@k); (f) calibration (Brier, reliability curves)
- **L1 Ground:** compute each on 10 predictions; see how one outlier moves RMSE but not MAE.
- **L2 Build:** choosing a loss that matches the business asymmetry, quantile regression for intervals, calibration checking and fixing (isotonic/Platt).
- **L3 Edge:** Recall@k and NDCG in depth — **these are the metrics you will use to evaluate retrieval in Week 27–28**, so they're taught properly here; proper scoring rules; prediction intervals via conformal prediction.
- **Hands-on:** build a reliability diagram for an XGBoost model, then calibrate it and show the improvement in Brier score.

### `P3-W19-M3` — Validation strategy
- Micro-lessons: (a) hold-out; (b) K-fold; (c) stratified K-fold; (d) group K-fold; (e) time-series splits; (f) nested CV
- **L1 Ground:** the same model scored by a single split vs 5-fold — see the variance in the estimate.
- **L2 Build:** choosing the split that matches how the model will be used (grouped by customer, forward in time), repeated CV for stable estimates, CV for hyperparameter search vs for final estimation.
- **L3 Edge:** nested CV to get an unbiased estimate when you also tuned; the cost (k×k fits) and when to accept the bias instead; CV variance and how many folds is enough; adversarial validation to detect train/test distribution mismatch.
- **Hands-on:** run adversarial validation on a train/test pair and identify the shifting features.

### `P3-W19-M4` — Data leakage: the career-defining failure mode
- Micro-lessons: (a) what leakage is; (b) target leakage; (c) train-test contamination; (d) temporal leakage; (e) group leakage; (f) leakage in preprocessing
- **L1 Ground:** a dataset with an obvious leak that gives 99.8% accuracy — find it.
- **L2 Build:** a leakage audit checklist; the "would this be available at prediction time?" test applied per feature; pipelines as structural protection; feature-generation windows for time-series.
- **L3 Edge:** subtle leaks — target encoding without out-of-fold, duplicate rows across splits, oversampling before splitting, normalization statistics from the full set, embeddings trained on test data; each demonstrated with the exact inflation it produces.
- **Hands-on:** five datasets, each with a different hidden leak; find and quantify each (accuracy before/after the fix).

### `P3-W19-M5` — Model selection, error analysis & reporting
- Micro-lessons: (a) baselines that matter; (b) statistical comparison of models; (c) error analysis by slice; (d) fairness slicing; (e) model cards; (f) when to ship
- **L1 Ground:** always beat: majority class, simple heuristic, and last-value baselines before celebrating.
- **L2 Build:** slice-based error analysis to find where the model fails, bootstrap CIs on the metric difference (using Week 12), a reproducible experiment log, model card authoring.
- **L3 Edge:** the offline/online gap; proxy metrics diverging from the business metric; shadow deployment and A/B testing a model (Week 12 again); regression testing for models — the direct ancestor of LLM evals in Week 31.
- **Hands-on:** produce a slice report showing a model that is 92% overall but 61% on a segment that is 30% of revenue; write the ship/no-ship recommendation.

### `LAB-P3-W19` — **Evaluation harness**
- `basic`: compute and plot the standard metric set for a provided model.
- `standard`: a reusable library — CV strategy selector, leakage audit checks, metric suite with bootstrap CIs, slice analysis, calibration, threshold optimizer, and an auto-generated HTML evaluation report; validated on 3 datasets.
- `hard`: nested CV + adversarial validation + automated leakage detection that catches all 5 planted leaks from M4; runtime budget enforced.
- **Ship it:** the harness is reused in the Midterm and referenced again in Week 31.

---

## T-P3-W20 — Week 20: Feature Engineering & Imbalanced Data

**Week outcome:** learner can turn raw data into features that move the metric, and handle the 1000:1 class ratio problems that dominate real business ML.

### `P3-W20-M1` — Numerical & categorical features
- Micro-lessons: (a) scaling (standard/min-max/robust); (b) transformations (log, Box-Cox, quantile); (c) binning; (d) one-hot vs ordinal; (e) target/mean encoding; (f) high-cardinality strategies (hashing, embeddings)
- **L1 Ground:** apply each encoder to a small table and look at the output columns.
- **L2 Build:** encoder choice per model family (trees don't need scaling; linear models do), out-of-fold target encoding done correctly, rare-category grouping, unseen-category handling at inference.
- **L3 Edge:** target encoding's leakage math and smoothing formula derived; hashing-trick collision analysis; entity embeddings for categoricals (bridge to Phase 4 embeddings); cardinality explosion and memory.
- **Hands-on:** implement out-of-fold target encoding from scratch; show the accuracy inflation of the naive version.

### `P3-W20-M2` — Temporal, text & interaction features
- Micro-lessons: (a) datetime decomposition & cyclical encoding; (b) lags, rolling windows, expanding stats; (c) TF-IDF & bag-of-words; (d) interactions & ratios; (e) aggregations across related tables; (f) domain features
- **L1 Ground:** turn a timestamp into 8 useful features.
- **L2 Build:** point-in-time-correct aggregations (no future data), rolling features with proper windows, TF-IDF for a text column feeding a tabular model, cross-table aggregation patterns from SQL (Week 7 pays off).
- **L3 Edge:** feature stores — training/serving skew and why it's the #1 production ML bug; computing the same feature in batch and online; TF-IDF vs embeddings compared on the same task, with cost and latency (sets up the sparse-vs-dense debate in Week 28).
- **Hands-on:** build a feature with a subtle point-in-time bug; detect it via a backtest; then fix it.

### `P3-W20-M3` — Feature selection & dimensionality
- Micro-lessons: (a) filter methods; (b) wrapper methods (RFE); (c) embedded methods (L1, tree importance); (d) permutation importance; (e) multicollinearity/VIF; (f) stability of selection
- **L1 Ground:** drop the 20 least useful features and see the score barely move.
- **L2 Build:** a selection workflow that doesn't leak (selection inside CV), permutation importance with correlated features, cost-aware selection (features that are expensive to compute at serving time).
- **L3 Edge:** correlated-feature importance splitting, SHAP vs permutation vs impurity compared on the same model, selection stability across bootstraps, and the maintenance cost of every feature you keep.
- **Hands-on:** cut a 200-feature model to 25 features with <1% metric loss; report the serving-latency win.

### `P3-W20-M4` — Imbalanced classification
- Micro-lessons: (a) why imbalance breaks defaults; (b) resampling (over/under); (c) SMOTE and variants; (d) class weights & cost-sensitive learning; (e) threshold tuning; (f) anomaly-detection framing
- **L1 Ground:** a 99.8%-accurate model that catches zero fraud — see the confusion matrix.
- **L2 Build:** resampling *inside* the CV fold only, `scale_pos_weight`, threshold selection from the PR curve against a business cost function, when to treat it as anomaly detection instead.
- **L3 Edge:** SMOTE's failure in high dimensions and on categorical features (with a measured counterexample); does resampling actually beat threshold tuning? — run the experiment; calibration destroyed by resampling and how to restore it.
- **Hands-on:** head-to-head: class weights vs SMOTE vs undersampling vs threshold-only, on the same data with the same budget; report the winner with CIs.

### `P3-W20-M5` — Production feature pipelines
- Micro-lessons: (a) `Pipeline`/`ColumnTransformer` end to end; (b) custom transformers; (c) serialization & versioning; (d) train/serve consistency; (e) monitoring feature drift; (f) documentation
- **L1 Ground:** wrap all preprocessing into one fitted object saved to disk.
- **L2 Build:** custom transformers with proper `fit`/`transform` separation, pinned versions, schema validation at inference, drift monitors on input distributions, a feature dictionary document.
- **L3 Edge:** pickle's fragility across versions (demonstrated by breaking it) and safer alternatives (ONNX, skops, plain-code transforms); latency budget per feature; the design of a minimal feature store.
- **Hands-on:** break a pickled pipeline by bumping a library version, then re-architect so it survives.

### `LAB-P3-W20` — **Credit-card fraud detection**
- `basic`: train a baseline on the imbalanced dataset; produce a PR curve.
- `standard`: full pipeline — leakage-free preprocessing, engineered temporal/aggregate features, XGBoost with `scale_pos_weight`, PR-curve threshold optimization against an explicit cost matrix, calibrated probabilities, slice analysis, and a report stating expected annual savings.
- `hard`: hit a target recall at a fixed false-positive budget; add drift monitoring and a serialization strategy that survives a dependency upgrade; sub-10 ms per-prediction latency including feature computation.
- **Ship it:** repo + cost analysis. Pairs with the Week-19 harness.

---

## T-P3-W21 — Week 21: Neural Networks & Backpropagation

**Week outcome:** learner builds a working autograd engine and neural net from scratch — so that nothing in Phase 4 is magic.

### `P3-W21-M1` — From linear models to neural networks
- Micro-lessons: (a) the perceptron; (b) why linear models can't do XOR; (c) hidden layers & non-linearity; (d) activations (sigmoid/tanh/ReLU/GELU); (e) universal approximation; (f) network anatomy
- **L1 Ground:** try to separate XOR with a line, fail, then add a hidden layer and succeed.
- **L2 Build:** layer sizing intuition, activation choice and its consequences (dead ReLUs, vanishing sigmoid gradients), output layer + loss pairings for regression/binary/multiclass.
- **L3 Edge:** universal approximation says nothing about learnability or efficiency; depth vs width expressivity; GELU/SwiGLU as used in modern LLMs and why (forward link to Week 25).
- **Hands-on:** plot the decision boundary as hidden units go 1 → 2 → 8 → 64; observe capacity and overfitting.

### `P3-W21-M2` — Forward pass, loss & backpropagation
- Micro-lessons: (a) forward pass as composed functions; (b) loss functions revisited; (c) the chain rule through a network; (d) backprop derivation layer by layer; (e) gradient checking; (f) computational graphs
- **L1 Ground:** a 2-input, 2-hidden, 1-output network computed entirely by hand — forward and backward, on paper.
- **L2 Build:** vectorized backprop for a 2-layer net in NumPy; matching shapes; the backward equations for linear, ReLU, sigmoid, softmax-cross-entropy.
- **L3 Edge:** build a **micrograd-style reverse-mode autograd engine** with a `Value`/`Tensor` class and topological-order backward — this is exactly what PyTorch does; memory cost of storing activations (the number behind Week 26's QLoRA memory math); gradient checkpointing explained.
- **Hands-on:** the autograd engine, plus `gradcheck` passing on a 3-layer network.

### `P3-W21-M3` — Training dynamics
- Micro-lessons: (a) initialization (Xavier/He); (b) vanishing & exploding gradients; (c) batch/layer normalization; (d) dropout; (e) learning-rate schedules & warmup; (f) reading loss curves
- **L1 Ground:** train the same net with zero-init, random-large-init, and He-init; watch three very different curves.
- **L2 Build:** a diagnostic playbook — loss not decreasing / decreasing then exploding / train-val gap / plateau — each with causes and fixes; BatchNorm vs LayerNorm and where each belongs; dropout placement.
- **L3 Edge:** why LayerNorm (not BatchNorm) is used in Transformers, with the sequence/batch reasoning; pre-norm vs post-norm stability; gradient-norm monitoring and clipping; the exact failure signatures of a bad learning rate in an LLM fine-tune (previews Week 26).
- **Hands-on:** deliberately induce and then diagnose 5 pathologies from their loss curves alone.

### `P3-W21-M4` — Optimizers & regularization in practice
- Micro-lessons: (a) SGD + momentum; (b) Adam/AdamW; (c) weight decay vs L2; (d) early stopping; (e) data augmentation; (f) hyperparameter priorities
- **L1 Ground:** the same net with SGD vs Adam; compare epochs to convergence.
- **L2 Build:** the tuning priority order (LR first, always), batch size vs LR scaling, AdamW as the modern default, augmentation as regularization.
- **L3 Edge:** Adam's optimizer state memory = 2× parameters — the arithmetic that decides whether you can fine-tune a 7B model on your GPU (Week 26); decoupled weight decay derivation; LR-range test; why the LLM world settled on AdamW + cosine + warmup.
- **Hands-on:** compute the full VRAM requirement for full fine-tuning of a 7B model (weights + grads + optimizer states + activations) and show why it exceeds a 24 GB GPU.

### `P3-W21-M5` — PyTorch fundamentals
- Micro-lessons: (a) tensors & devices; (b) autograd in PyTorch; (c) `nn.Module`; (d) `Dataset`/`DataLoader`; (e) the training loop; (f) saving/loading & reproducibility
- **L1 Ground:** rebuild your NumPy net in PyTorch in 30 lines and get the same result.
- **L2 Build:** a canonical training loop you'll reuse all of Phase 4 (train/val split, metrics, checkpointing, seed control, device handling, `no_grad` for eval), custom `Dataset`, `DataLoader` workers.
- **L3 Edge:** what `.backward()` does to the graph; `detach()`/`no_grad()`/`inference_mode()` differences; common silent bugs (forgetting `optimizer.zero_grad()`, `model.eval()`, non-determinism sources); `torch.compile` speedup measured; MPS/CUDA/CPU differences on Apple Silicon.
- **Hands-on:** write a training-loop template with checkpointing and resumption; kill it mid-epoch and resume without metric discontinuity.

### `LAB-P3-W21` — **`nanograd`: autograd + neural net from scratch**
- `basic`: 2-layer network in NumPy with hard-coded backprop, matching provided gradients.
- `standard`: a reverse-mode autograd engine (scalars or tensors), `Linear`/`ReLU`/`Softmax`/`CrossEntropy` modules, SGD + Adam, trained on MNIST to ≥95% test accuracy — with gradient checks and no deep-learning framework.
- `hard`: tensor-based autograd with broadcasting, plus a PyTorch parity test (same seed, same result within tolerance) and a speed comparison; add gradient checkpointing and measure the memory saving.
- **Ship it:** repo + a "how backprop actually works" explainer. One of the strongest portfolio pieces in the course.

---

## T-P3-W22 — Week 22: PyTorch, CNNs & Transfer Learning

**Week outcome:** learner trains a real computer-vision model to a stated accuracy bar and understands transfer learning — the same idea they'll apply to LLMs in Week 26.

### `P3-W22-M1` — Images as data & OpenCV
- Micro-lessons: (a) image representation (channels, dtype, ranges); (b) color spaces; (c) resizing, cropping, normalization; (d) filters & convolution by hand; (e) augmentation; (f) dataset structure
- **L1 Ground:** load an image, look at the array, apply a blur kernel manually.
- **L2 Build:** a preprocessing pipeline with correct normalization statistics, augmentation policy (and the ones that hurt), handling class-imbalanced image folders, `torchvision.transforms` v2.
- **L3 Edge:** convolution as matrix multiplication (im2col) — why GPUs love it; data-loading as the actual bottleneck (measure GPU utilization and fix an input-bound loop); JPEG artifacts and their effect on accuracy.
- **Hands-on:** profile a training loop that is 30% GPU-utilized; get it above 85% by fixing the data pipeline.

### `P3-W22-M2` — Convolutional neural networks
- Micro-lessons: (a) the convolution operation; (b) kernels, stride, padding, dilation; (c) feature maps & receptive fields; (d) pooling; (e) CNN architecture patterns; (f) parameter counting
- **L1 Ground:** apply a 3×3 edge-detector kernel by hand to a 5×5 image.
- **L2 Build:** design a CNN for a given input size, compute output shapes and parameter counts by hand (the skill that prevents 90% of shape errors), batch norm placement, global average pooling.
- **L3 Edge:** receptive-field arithmetic; 1×1 convolutions; depthwise-separable convs and the FLOP reduction computed; ResNet's skip connections and the gradient-flow argument — the same residual idea that makes Transformers trainable (Week 25).
- **Hands-on:** visualize learned first-layer filters and intermediate activations; explain what the network is detecting.

### `P3-W22-M3` — Training a CNN properly
- Micro-lessons: (a) dataset splits for images; (b) the training loop with metrics; (c) overfitting control; (d) mixed precision; (e) checkpointing & experiment tracking; (f) error analysis on images
- **L1 Ground:** train a small CNN on a small dataset end to end.
- **L2 Build:** a reproducible training script with config, logging, checkpoint-best, early stopping, AMP (`torch.amp`) for 2× speed, per-class metrics, confusion matrix over images.
- **L3 Edge:** mixed-precision numerics (FP16 overflow, GradScaler, BF16 on newer hardware) — direct groundwork for Week 26 quantization; throughput vs batch-size curve; multi-GPU concepts (DDP) and when it's worth it.
- **Hands-on:** measure training throughput and memory at FP32 vs AMP; report the speedup and any accuracy delta.

### `P3-W22-M4` — Transfer learning
- Micro-lessons: (a) why pre-trained features transfer; (b) feature extraction vs fine-tuning; (c) freezing & unfreezing schedules; (d) discriminative learning rates; (e) architecture choice (ResNet/EfficientNet/ViT); (f) domain gap
- **L1 Ground:** ResNet-18 frozen + a new head, trained in 5 minutes, beating your from-scratch CNN.
- **L2 Build:** the full recipe — replace head → train head → unfreeze gradually with lower LRs → evaluate; choosing a backbone by accuracy/latency/size; handling a large domain gap (medical, satellite).
- **L3 Edge:** what layers learn at each depth (with visualizations); catastrophic forgetting; **transfer learning here is conceptually identical to LLM fine-tuning in Week 26** — make the mapping explicit (frozen backbone ↔ frozen base weights, new head ↔ LoRA adapter); ViT vs CNN data-efficiency trade-off.
- **Hands-on:** compare from-scratch vs feature-extraction vs full fine-tune on the same small dataset; plot accuracy vs training time vs dataset size.

### `P3-W22-M5` — Beyond classification & model export
- Micro-lessons: (a) object detection & segmentation overview; (b) embeddings from a vision model; (c) similarity search on images; (d) `torch.save` vs TorchScript vs ONNX; (e) inference optimization; (f) fastai/Keras as higher-level options
- **L1 Ground:** extract a feature vector from an image and find its nearest neighbor.
- **L2 Build:** export to ONNX and run inference without PyTorch, measure size and latency; batching at inference; CPU inference tuning.
- **L3 Edge:** image embeddings + nearest neighbor = the *same* retrieval architecture as text RAG (Week 27), demonstrated on a real image search over 50k images; quantized inference preview; export pitfalls (dynamic shapes, unsupported ops).
- **Hands-on:** build an image similarity search over 50k images; report index build time, query latency and recall — a direct dry run for Week 27.

### `LAB-P3-W22` — **Blood-cell image classifier (≥90% test accuracy)**
- `basic`: train a provided CNN skeleton to a modest accuracy on a prepared split.
- `standard`: full project — dataset audit, augmentation policy, custom CNN baseline, then transfer learning (ResNet/EfficientNet) to ≥90% test accuracy, AMP, checkpointing, per-class metrics, confusion matrix, error analysis on the 20 worst misclassifications, model card.
- `hard`: ≥93% under a stated inference-latency budget on CPU, with ONNX export and a measured latency/size table; plus a Grad-CAM explanation of 5 predictions.
- **Ship it:** repo + deployed demo (the API comes next week).

---

## T-P3-W23 — Week 23: MLOps I — Packaging, Docker & Serverless

**Week outcome:** learner ships a model as a real, containerized, deployed service with health checks, tests and CI.

### `P3-W23-M1` — From notebook to service
- Micro-lessons: (a) why notebooks don't ship; (b) project structure; (c) model serialization (pickle/joblib/`state_dict`/ONNX); (d) inference code separated from training; (e) config & environment; (f) reproducibility
- **L1 Ground:** convert a notebook into `train.py` + `predict.py` + `model.pkl`.
- **L2 Build:** a repo layout that a team can work in, artifact versioning, deterministic training runs, dependency pinning with `uv`, separating training-time and serving-time dependencies (a 3 GB → 300 MB win).
- **L3 Edge:** pickle security (arbitrary code execution on load — demonstrate it safely) and safe alternatives; model registries; reproducibility across hardware (CUDA nondeterminism); the artifact lineage you need for an audit.
- **Hands-on:** make a training run bit-for-bit reproducible; document every source of nondeterminism you had to pin.

### `P3-W23-M2` — Serving with FastAPI
- Micro-lessons: (a) prediction endpoints; (b) Pydantic schemas for model I/O; (c) model loading at startup; (d) batching; (e) health/readiness endpoints; (f) errors, timeouts & versioning
- **L1 Ground:** wrap the Week-20 model in the Week-6 FastAPI patterns; POST features, get a prediction.
- **L2 Build:** load once at startup (not per request), input validation mirroring training schema, request batching for throughput, `/healthz` + `/ready`, model version in the response, graceful degradation.
- **L3 Edge:** measured throughput: per-request vs micro-batched inference; thread/process configuration for CPU inference (`torch.set_num_threads` and the oversubscription trap from Week 4); p99 latency under load; warm-up requests.
- **Hands-on:** load-test the service; produce an RPS vs p99 curve; find and fix the bottleneck; re-measure.

### `P3-W23-M3` — Docker
- Micro-lessons: (a) images vs containers; (b) Dockerfile basics; (c) layer caching; (d) multi-stage builds; (e) volumes, networks, `docker compose`; (f) image size & security
- **L1 Ground:** containerize a hello-world API and run it.
- **L2 Build:** a multi-stage Dockerfile taking the ML image from 3 GB to <500 MB, layer ordering for fast rebuilds, `.dockerignore`, non-root user, `compose` for API + Postgres, environment configuration, healthchecks.
- **L3 Edge:** layer caching mechanics and build-time measurements before/after optimization; slim vs alpine vs distroless (and the glibc/musl trap with NumPy wheels); image scanning for CVEs; reproducible builds; BuildKit cache mounts for pip/uv.
- **Hands-on:** take a provided 4 GB image to under 600 MB and cut rebuild time by 80%; document each change and its saving.

### `P3-W23-M4` — CI/CD
- Micro-lessons: (a) GitHub Actions basics; (b) test + lint + type gates; (c) building & pushing images; (d) environments & secrets; (e) deploy on merge; (f) rollback
- **L1 Ground:** a workflow that runs your tests on every push.
- **L2 Build:** a full pipeline — lint, type-check, unit tests, build image, push to a registry, deploy; caching for speed; branch protection; secrets handled properly; a smoke test after deploy.
- **L3 Edge:** pipeline runtime budget and parallelization; matrix builds; the *model* CI problem — how do you test a model? (data tests, performance thresholds, no-regression gates) — the direct precursor of Week 31's eval CI.
- **Hands-on:** add a CI gate that fails the build if model accuracy on a fixed holdout drops more than 1% versus the committed baseline.

### `P3-W23-M5` — Serverless deployment
- Micro-lessons: (a) serverless model & trade-offs; (b) AWS Lambda + container images; (c) API Gateway; (d) cold starts; (e) limits (size, memory, timeout); (f) cost model
- **L1 Ground:** deploy a trivial function and call it over HTTP.
- **L2 Build:** package the model as a Lambda container image, IAM basics, API Gateway routing, environment config, logging to CloudWatch, staying inside the free tier.
- **L3 Edge:** cold-start measurement and mitigation (provisioned concurrency, smaller images, lazy loading), the cost crossover between Lambda and a always-on container computed for a given RPS, when serverless is wrong for ML (large models, GPU, long inference).
- **Hands-on:** measure cold vs warm latency across 3 image sizes; compute the monthly cost at 10 / 1k / 100k requests per day for Lambda vs a small VM, and state the crossover.

### `LAB-P3-W23` — **Containerized prediction service → serverless**
- `basic`: FastAPI wrapper + Dockerfile that runs locally.
- `standard`: production-grade service — versioned model artifact, validated I/O, health checks, tests, multi-stage image <600 MB, `docker compose` stack, GitHub Actions CI building and pushing, deployed to AWS Lambda behind API Gateway, with a load-test and cost report.
- `hard`: p95 < 300 ms including cold-start mitigation; add a canary deployment and an automatic rollback on error-rate threshold.
- **Ship it:** live URL + `DEPLOYMENT.md` with the architecture diagram and cost analysis.

---

## T-P3-W24 — Week 24: MLOps II — Kubernetes & Model Serving

**Week outcome:** learner deploys a horizontally scaling model service on Kubernetes and can reason about it under load and failure.

### `P3-W24-M1` — Why orchestration exists
- Micro-lessons: (a) the problems K8s solves; (b) architecture (control plane, nodes, kubelet); (c) Pods; (d) declarative vs imperative; (e) `kubectl` basics; (f) local clusters with `kind`
- **L1 Ground:** spin up `kind`, run your Week-23 image as a Pod, port-forward and call it.
- **L2 Build:** the reconciliation loop mindset, YAML structure, namespaces, labels and selectors, debugging with `describe`/`logs`/`events`/`exec`.
- **L3 Edge:** the control-plane flow when you `kubectl apply` (API server → etcd → scheduler → kubelet); when K8s is overkill (with an honest decision table vs Lambda, ECS, a VM); the operational cost you're signing up for.
- **Hands-on:** break a Pod five ways (bad image, OOM, failing probe, missing config, insufficient resources) and diagnose each from `kubectl` output alone.

### `P3-W24-M2` — Deployments, Services & configuration
- Micro-lessons: (a) ReplicaSets & Deployments; (b) rolling updates & rollback; (c) Services (ClusterIP/NodePort/LoadBalancer); (d) Ingress; (e) ConfigMaps & Secrets; (f) liveness/readiness/startup probes
- **L1 Ground:** deploy 3 replicas behind a Service; delete a Pod and watch it come back.
- **L2 Build:** full manifests for the model service, rolling update with zero dropped requests (requires the graceful shutdown from Week 6), probe design that doesn't cause restart loops, config/secret injection, `maxSurge`/`maxUnavailable`.
- **L3 Edge:** why readiness probes must not check downstream dependencies; `preStop` hooks and connection draining; the exact sequence that causes 502s during a deploy, demonstrated and then fixed; secret management beyond base64 (external secret stores).
- **Hands-on:** run a continuous load test through a rolling update; prove zero failed requests, then break it deliberately and explain the failure.

### `P3-W24-M3` — Resources, scheduling & autoscaling
- Micro-lessons: (a) requests vs limits; (b) QoS classes & OOMKilled; (c) HPA on CPU/memory; (d) custom metrics; (e) cluster autoscaling; (f) capacity planning
- **L1 Ground:** set requests/limits and watch a Pod get throttled, then OOMKilled.
- **L2 Build:** sizing requests from measured usage, HPA configuration with sensible thresholds and stabilization windows, load-testing the scale-up, PodDisruptionBudgets.
- **L3 Edge:** CPU throttling and its effect on p99 (measured); why memory limits are hard and CPU limits are soft; scaling latency (metric interval → HPA loop → Pod start → readiness) computed end to end; queue-depth-based scaling as the right signal for ML inference; GPU scheduling basics.
- **Hands-on:** produce a scaling report: apply increasing load, plot replicas / latency / error rate over time, and identify the lag windows.

### `P3-W24-M4` — Model-serving frameworks
- Micro-lessons: (a) custom API vs dedicated servers; (b) TensorFlow Serving; (c) TorchServe / Triton overview; (d) model versioning & A/B routing; (e) dynamic batching; (f) GPU serving basics
- **L1 Ground:** serve a saved model with TensorFlow Serving and call its REST endpoint.
- **L2 Build:** deploy TF Serving on K8s with a model volume, version routing, dynamic batching configuration, comparing against your FastAPI service on throughput and latency.
- **L3 Edge:** dynamic batching's latency/throughput trade-off measured (the same mechanism as vLLM's continuous batching in Week 26); gRPC vs REST payload/latency comparison; multi-model serving and memory pressure; shadow traffic for safe model rollout.
- **Hands-on:** benchmark FastAPI vs TF Serving at batch sizes 1/8/32; produce the table and a recommendation with a stated regime for each.

### `P3-W24-M5` — Operating an ML service
- Micro-lessons: (a) metrics that matter; (b) Prometheus + Grafana basics; (c) logging & tracing; (d) alerting & SLOs; (e) drift & performance monitoring; (f) incident response & runbooks
- **L1 Ground:** expose a `/metrics` endpoint and see request counts in Grafana.
- **L2 Build:** the four golden signals for a model service, plus ML-specific monitors (input drift, prediction distribution shift, feature nulls); SLO definition and error budget; a runbook for "model returns garbage".
- **L3 Edge:** detecting silent model degradation without labels (proxy signals, delayed-label pipelines); alert fatigue and alerting on symptoms not causes; a post-mortem template — all of which is reused verbatim for LLM systems in Week 32.
- **Hands-on:** write the runbook and then run a game-day: a teammate breaks the service, you diagnose it using only dashboards and logs.

### `LAB-P3-W24` — **Kubernetes model-serving cluster**
- `basic`: Deployment + Service for the Week-23 image on `kind`, reachable via port-forward.
- `standard`: full manifests (Deployment, Service, Ingress, ConfigMap, Secret, probes, resources), HPA scaling on load, TensorFlow Serving deployment alongside the FastAPI one, Prometheus metrics + Grafana dashboard, and a load-test report showing scale-up behaviour.
- `hard`: zero-downtime rolling update under sustained load with proof; queue-depth-based custom-metric autoscaling; documented p50/p95/p99 at 3 load levels with a cost-per-1M-predictions estimate.
- **Ship it:** repo + `RUNBOOK.md` + scaling report.

---

## `T-P3-MID` — Midterm Project: End-to-End Classical ML System
*(2-week overlay, runs alongside Weeks 23–24; defended at the end of Week 24)*

**Brief:** choose a real, messy, publicly available dataset (not a cleaned Kaggle competition set). Ship a system, not a notebook.

**Required deliverables**
1. Problem framing document — the decision the model serves, the cost of each error type, the baseline to beat.
2. Ingestion + EDA using the Week 15–16 tooling.
3. Leakage-free feature pipeline with custom transformers.
4. At least 3 modelled approaches with a defensible validation strategy and CIs on the comparison.
5. Threshold/decision policy tied to the stated costs.
6. Model card + slice/fairness analysis.
7. FastAPI service, multi-stage Docker image, CI pipeline with a model-quality gate.
8. Kubernetes deployment with HPA + monitoring dashboard.
9. Load test and cost-per-prediction analysis.
10. A 15-minute defence: architecture walkthrough + hostile Q&A.

**Rubric (100 pts):** framing 10 · data work 15 · modelling 15 · evaluation rigor 20 · engineering 20 · deployment/ops 10 · communication 10.
**Anti-patterns that cap the grade:** any leakage, any unversioned artifact, any metric without a CI or baseline, any "it works on my machine".

---

## Phase 3 exit checkpoint (gate to Phase 4)

1. Derive backprop for a 2-layer network on a whiteboard.
2. Given a dataset and a business goal, produce a defensible model + evaluation in 4 hours.
3. Find the planted leak in an unfamiliar pipeline.
4. Take a model from `model.pkl` to a scaling K8s deployment in one working day.
5. Explain the VRAM arithmetic of training a model — the prerequisite for every decision in Phase 4.
