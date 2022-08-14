# Auto Evaluation of Programs

## Project Goal
Automatic evaluation of Computer Programs
The final goal is to create an application to automate the process of evaluation. This is achieved by leveraging powerful techniques like symbolic execution and bounded model checking. Here we will be using a symbolic execution engine, KLEE, built on top of the LLVM compiler infrastructure, and a bounded model checker, CBMC, for C/C++ programs. These statically analyze code and generate a set of test cases

### Installing the project
clone this repo into your system
```bash
git clone https://github.com/AutoEvalOrg/Grader.git
```
### virtual environment
Setup virtual environment
```bash
cd Grader/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Deactivating virtual environment 
```bash
deactivate
```

### Prerequisites
Some prior experience in programming languages like Python
