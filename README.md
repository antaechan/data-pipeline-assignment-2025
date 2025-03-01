# data-pipeline-assignment-2025

이 리포지토리는 [cell2info.gz](https://ftp.ncbi.nlm.nih.gov/pubchem/Target/cell2info.gz) 파일을 기반으로 한 Datapipeline 과제 안내를 목적으로 한다.

## 과제 목표

1. **데이터 파이프라인 구현 (필수)**  
   - 데이터 다운로드, 데이터 프로세싱, 데이터 저장의 파이프라인을 구성한다.

2. **비지니스 로직 검증용 테스트 코드 작성 (선택)**  
   - 작성 코드를 검증하기 위한 테스트 코드를 작성한다.

3. **GitHub Actions를 활용한 CI/CD (선택)**  
   - 코드 커밋 시 자동화된 테스트 및 빌드를 수행하는 CI/CD 파이프라인을 구성한다.


## 과제 구현 사항

### 1. 데이터 파이프라인

- #### 1-1. 데이터베이스 스키마 설계 (필수)
  모든 행과 열의 데이터를 포함하면서 제 2정규화를 만족하도록 Schema를 설계 하여야 한다. 컬럼명은 해당 테이블의 첫 번째 열을 참고하여 지정한다.

  - **cells 테이블:**  
    `cell_id` 컬럼을 PRIMARY KEY로 지정

  - **taxonomy table:**  
    `taxonomy_id` 컬럼을 PRIMARY KEY로 지정

  - **synonyms 테이블:**  
    row 를 PRIMARY KEY로 지정

- #### 1-2. 데이터베이스 파이프라인 구현 (필수)
  [cell2info.gz](https://ftp.ncbi.nlm.nih.gov/pubchem/Target/cell2info.gz) 링크에서 파일을 다운로드 받은 후, 최종적으로 `./db` 폴더에 sqllite3 Database에 데이터 저장하여야 한다.


### 2. 비지니스 로직 검증용 테스트 코드 작성 

- 작성한 함수에 대해서 테스트 코드를 작성하여 비지니스 로직 검증하여야 한다. 테스트 방식 등은 자유롭게 설정할 수 있다.

### 3. GitHub Actions를 활용한 CI/CD

- **자동화 파이프라인 구성:**  
  - `.github/workflows/ci-cd.yml` 파일에 정의된 워크플로우를 통해 커밋 시 자동으로 테스트, 빌드 과정을 수행하여야 한다.



## 제출 방법 및 구성

해당 과제 완료 후 공개된 github 레포지토리 링크 제출한다. 이 때, `./db` 폴더에 Database가 저장되어있어야 한다.



## 주의 사항
- **README 작성:**  
  과제 제출 시 솔루션의 내용을 README에 기입하여야 한다.

- **환경 설정:**  
  해당 프로젝트를 구현하는데 사용한 여러 환경 설정을 재현할 수 있어야 한다. 해당 사항을 README에 기입하거나, DockerFile을 활용하여 가능하도록 해야한다.


## 권장 사항

- **구현 방식 및 언어**  
  구현 언어 : `Python`  
  구현 방식 : `Airflow`