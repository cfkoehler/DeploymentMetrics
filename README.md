# DeploymentMetrics
## Calculate Basic Software Deployment metrics
- Deployment Frequency
- Change Failure Rate

## Provide a deployments.csv file formatted in four columns:
- version
- secondaryDeployment (Not currently used)
- pirmaryDeployment
- failure (Deployment requires either a rollback or patch within in 24 hours)

**Sample deployments.csv:**
```
version,secondaryDeployment,pirmaryDeployment,failure
1.0.0,11/22/22,11/23/22,false
1.1.0,11/24/22,11/25/22,false
1.2.0,11/26/22,NA,false
```

## Steps to create a virtual environment and run:
To create virtual env: `python -m venv env`<br>
To activate virtual env: `source env/bin/activate` <br>
Install required pip packages: `pip3 install -r requirements.txt` <br>
Run: `python3 generate_metrics.py`

## Future work:
- [ ] Write sample github actions .yml file to update csv and generate images
- [ ] Write sample gitlab runner ci file to update csv and generate images
- [ ] Accept number of code commits per release as value and add to plot
- [ ] Display frequency trends on charts
- [ ] Display rolling average of frequency to show trends in designated time frame