## Repository:

### 1. **GitHub** - branches structure:
- 1.1 - piotr - production branch
- 1.2 - feature - feature branch (name format: {*developer_name.title()*}_{*branch_developer_id*}_{*feature_description*} e.g. *Piotr_1_pse_data_scrapper* 
- 1.3 create new branch from dev branch: 
  - git checkout -b brach_name
- 1.4 rebase branch: 
  - git fetch origin dev:dev
  - git rebase dev
  - code version selection
  - git add .
  - git rebase --continue
  - code version selection
  - git add .
  - git push -f origin branch_name

### 2. **Git Bash/ PyCharm** - commits:
- 2.1 git add .
- 2.2 git commit -m "commit description" # meaningful commit's description; "wip/./sth" not accepted!
- 2.3 git push origin feature branch e.g. git push origin adam_1_pse_data_scrapper 

### 3. **GitHub** - pull Requests:
- 3.1. PR description as *bullet point list* required
- 3.2. Assign *Piotr Średnicki* as **required reviewer**, rest developers as **optional reviewers**
- 3.3. Merge from feature into dev accepted if PR receive approve vote and all comments/threads are resolved

### 4. **PyCharm** - docstring format:
- 4.1 Function:
```
def function(x, y, z):
    """
    Function calculates weighted rolling mean
    Arguments:
        x: pd.DataFrame
        y: int
        z: str
    Returns:
        Function returns pd.DataFrame with calculated weighted rolling means
    """
    
    # code block
    
    return ...
```
- 4.2 Class:
```
class Class:
    """
    Class builds Pyomo optimization model
    Arguments:
        x: pd.DataFrame
        y: int
        z: str
    """
    
    def __init__(self, ...):
        self.x = x
        self.y = y
        self.z = z
        
    def method(self, sense, solver):
        """
        Method starts Mixed Integer Linear Programming optimization model 
        Arguments:
            sense: str ["minimize", "maximize"]
            solver: str ["glpk", "cbc", "cplex", "ipopt"]
        Returns:
            Optimized transportation delivery schedule
        """
        
        # code block
        
        return ...
```

### 5. **PyCharm** - typing:
- 5.1 Build-in types
- 5.2 Package *typing*
```
def function(tbl: pd.DataFrame,
             n: int, 
             type: str) -> pd.DataFrame:
    """
    docstring
    """
    
    # code block
    
    return tbl
```

### 6. **PyCharm** - logging:
```
def function():
    """
    docstring
    """

    logging.info("")    
    logging.warning("")
    logging.debug("")
    logging.error("")
    logging.critical("")
    
    # code block
    
    return ...
```

### 7. **PyCharm** - useful tips:
- 7.1 ```# !TODO(AN)``` - to do author notes in code
- 7.2 Reformat .py file according to PEP-8: ctrl+A -> ctrl+shift+alt+L -> enter
