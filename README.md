# FHE-Based Biological Age and Aging Pace Estimator

This repository implements a privacy-preserving biological age and aging pace estimator using Zama's [Concrete ML](https://github.com/zama-ai/concrete-ml) Fully Homomorphic Encryption (FHE) library.

- **All computations on sensitive data are performed encrypted (FHE).**
- **Model is demonstrated on real methylation data (GSE40279).**
- **Client/server demo is ready for local use and Hugging Face Spaces deployment.**

## How It Works
1. **Model**: A LinearRegression model is trained on real methylation data (5 CpGs) to predict biological age.
2. **FHE**: The model is compiled for FHE inference using Concrete ML.
3. **Client/Server**: Client encrypts input, server predicts on encrypted data, client decrypts result.
4. **Demo**: Deployable to Hugging Face Spaces or can be run locally.

## Usage

1. **Install dependencies:**

 ```bash
 pip install -r requirements.txt
 ```

 **Install ZAMA Concrete ML Library**

Concrete ML can be installed via pip on Linux and macOS (Intel or Apple Silicon).  
**Note:** Windows users should use WSL or Docker (see [Zama docs](https://docs.zama.ai/concrete-ml/get-started/pip_installing)).

```bash
pip install concrete-ml
```
If you encounter installation issues (e.g., unsupported CPU or AVX2 limitations), refer to:

- 📦 [Concrete ML on PyPI](https://pypi.org/project/concrete-ml/)
- 📘 [Zama Concrete ML Installation Guide](https://docs.zama.ai/concrete-ml/get-started/pip_installing)

### Docker Alternative

If you prefer Docker or are on Windows, you can use the official Docker image:

```bash
docker pull zamafhe/concrete-ml:latest
```

See [official Docker instructions](https://docs.zama.ai/concrete-ml/get-started/pip_installing) for more details.

> For more help, see the [Concrete ML documentation](https://docs.zama.ai/concrete-ml) or [Zama’s GitHub](https://github.com/zama-ai/concrete-ml).```


2. **Train model:**

 ```bash
 python src/train.py
 ```

3. **Run client/server demo:**

```bash
python src/app/server.py
python src/app/client.py
```

Try sample input from `data/bio_age_demo_data.csv`(5 methylation values, 0–1 scale)

## FHE Biological Age Estimation Report

### 1. Data Pipeline
- Source: GSE40279 (656 blood samples)
- CpGs: ELOVL2 (cg16867657), KLF14, TRIM59, FHL2, CCDC102B
- Age range: 62-89 years

### 2. Model Architecture
- Type: LinearRegression (FHE-compatible)
- Quantization: 8-bit weights/activations
- FHE Params: p_error=0.03, global_p_error=0.01

## 3. Performance

> All metrics measured on local machine (Intel CPU with AVX2 support) using Concrete-ML 1.9.0.

### 🚦 Performance Benchmarks

| Metric                | Cleartext Value | FHE Value           | 
|-----------------------|-----------------|---------------------|
| MAE (years)           | 5.02            | 5.02                |
| R²                    | 0.83            | 0.83                |
| Inference time/sample | 0.33–0.57 ms    | 0.02–0.05 s         |
| Model type            | LinearRegression| LinearRegression    |
| Data                  | GSE40279, n=656 | GSE40279, n=656     |


## 4. Security
- Key size: 128-bit
- Cryptographic parameters: TFHE shortint

## 5. Deployment

- **Local demo:** See Usage above.
- **Hugging Face Spaces:** **[vamshi257/fhe-bio-age-estimator](https://huggingface.co/spaces/vamshi257/fhe-bio-age-estimator/tree/main)**

## 6. References

- [Zama Concrete ML](https://github.com/zama-ai/concrete-ml)
- [GSE40279 dataset](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE40279)
- [dnaMethyAge R package](https://github.com/yiluyucheng/dnaMethyAge)

---
