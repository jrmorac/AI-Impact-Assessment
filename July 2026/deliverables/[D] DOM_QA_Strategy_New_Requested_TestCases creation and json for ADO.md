# DOM QA Strategy, New Test Cases, and ADO Import Content Summary

## Strategy Summary

### Azure Coverage
Azure is treated as a first-class testable component and includes:
- Terraform infrastructure provisioning validation
- Resource creation verification
- Security and compliance pipeline validation
- CI/CD deployment verification
- Post-deployment smoke testing

### Security Coverage
Security coverage includes:
- HITRUST HIPAA pipeline validation
- Checkov Terraform security scans
- Fortify SAST validation
- Trivy container security validation
- Azure policy compliance validation
- Role-based access control testing

### Access Control Coverage
Roles covered:
- Admin
- User
- Customer

Validation includes:
- Admin access to privileged functions
- User restrictions
- Customer access limitations
- Hidden UI functionality for unauthorized users

### Deployment Coverage
Additional deployment testing includes:
- Code deployment validation
- Production smoke testing
- Infrastructure verification
- Compliance verification

### Performance Coverage
Performance validation includes:
- Large file upload testing
- Ingestion runtime benchmarking
- Stability testing under load

---

# New Requested Test Cases

## **Azure – Terraform / Infrastructure Provisioning**

1. **Azure – Terraform – Generate deployment plan successfully**

   * Verify Terraform plan is generated in Azure DevOps without errors  
   * Verify no policy or validation blockers are reported  
2. **Azure – Terraform – Shared resource group is created**

   * Verify shared resource group exists  
   * Verify correct region, naming convention, and tags applied  
3. **Azure – Terraform – Network resources are provisioned**

   * Verify VNet creation  
   * Verify subnet configuration  
   * Verify application gateway / load balancer exists  
4. **Azure – Terraform – Shared data services are provisioned**

   * Verify shared SQL database exists  
   * Verify Databricks workspace / cluster exists  
   * Verify UI / API container apps are deployed  
5. **Azure – Terraform – Security resources are provisioned**

   * Verify Key Vault is created  
   * Verify secrets are populated  
   * Verify access permissions granted to expected services  
6. **Azure – Terraform – Client resource group is created**

   * Verify client resource group exists  
   * Verify naming and isolation from other clients  
7. **Azure – Terraform – Client data resources are created**

   * Verify client SQL database  
   * Verify client Databricks cluster  
   * Verify storage account exists  
8. **Azure – Terraform – Project customer container is created**

   * Verify project–customer container exists  
   * Verify container is mapped to correct client/project  
9. **Azure – Terraform – Apply execution completes successfully**

   * Verify Terraform apply finishes without errors  
   * Verify final pipeline summary reports success

*Tag suggestion:* `Azure_Terraform`

---

## **Azure – CI/CD & Code Deployment**

1. **Azure – CI/CD – Code deployment pipeline executes successfully**

   * Verify CI/CD pipeline runs to completion  
   * Verify no failed or skipped stages  
2. **Azure – CI/CD – Deployed version matches expected build**

   * Verify deployed build/version matches release artifacts  
3. **Azure – CI/CD – Smoke test after deployment**

   * Verify portal is accessible  
   * Verify API responds successfully  
   * Verify no critical errors in logs

*Tags:* `Code_Deployment_Testing`

---

## **Security / HITRUST Verification**

1. **Security – HITRUST – HIPAA report pipeline executes successfully**

   * Verify MediQuant HITRUST HIPAA pipeline runs  
   * Verify compliant / pass result is recorded  
2. **Security – Terraform – Checkov scan executes successfully**

   * Verify Checkov scan runs during IaC pipeline  
   * Verify results reviewed and no critical failures remain  
3. **Security – Application – Fortify scan executes successfully**

   * Verify Fortify SAST scan runs in web/API pipeline  
   * Verify results are attached to the run  
4. **Security – Containers – Trivy scan executes successfully**

   * Verify Trivy security scan runs  
   * Verify no critical vulnerabilities remain unresolved  
5. **Security – Azure – Policy compliance check passes**

   * Verify Azure policy compliance executed  
   * Verify non‑compliant resources are flagged or blocked

*Tags:* `Security_HiTrust`

---

## **User Security / Role‑Based Access Control**

1. **Security – RBAC – Admin has full portal access**

   * Verify admin can manage customers  
   * Verify admin can manage projects  
   * Verify admin can access Legacy Systems  
2. **Security – RBAC – User access restrictions enforced**

   * Verify user cannot create or edit customers  
   * Verify user can access permitted features  
3. **Security – RBAC – Customer has no portal access**

   * Verify customer role cannot access operational portal  
   * Verify access is denied at login or navigation level  
4. **Security – RBAC – Restricted UI elements are hidden**

   * Verify restricted links and actions are not visible to non‑authorized roles

*Tag:* `Access_Control`

---

## **Post‑Production Deployment**

1. **Post Deployment – Infrastructure – Resources exist**

   * Verify required Azure resources exist post‑deployment  
2. **Post Deployment – Security – Compliance checks pass**

   * Verify security and HITRUST pipelines completed successfully  
3. **Post Deployment – Smoke – Application is operational**

   * Verify portal access  
   * Verify API connectivity  
   * Verify no blocking production errors

*Tag:* `Post_Deployment_Smoke`

---

## **Performance / Benchmarking**

1. **Performance – File Upload – Large file uploads within acceptable time**

   * Upload known large dataset  
   * Verify upload completes within expected timeframe  
2. **Performance – Ingestion – Pipeline completes within baseline**

   * Execute ingestion using benchmark dataset  
   * Compare runtime against February baseline results  
3. **Performance – Stability – No failures under large data load**

   * Verify pipeline completes without errors  
   * Verify no resource exhaustion observed

*Tag:* `Performance_Baseline`

---

# ADO Import CSV Content

ID,Work Item Type,Title,Test Step,Step Action,Step Expected,Area Path,Tags,Assigned To,State
,Test Case,Azure - Terraform - Generate deployment plan successfully,,,,Data Platform,Azure_Terraform,,Design
,,,"1","Trigger Azure DevOps Terraform pipeline","Terraform plan is generated successfully with no validation or policy errors",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - Terraform - Shared resource group is created,,,,Data Platform,Azure_Terraform,,Design
,,,"1","Execute Terraform apply pipeline","Shared resource group is created with correct naming region and tags",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - Terraform - Network resources are provisioned,,,,Data Platform,Azure_Terraform,,Design
,,,"1","Execute Terraform apply pipeline","VNet subnets and application gateway or load balancer exist",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - Terraform - Shared data services are provisioned,,,,Data Platform,Azure_Terraform,,Design
,,,"1","Execute Terraform apply pipeline","Shared SQL database Databricks workspace and container apps are deployed",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - Terraform - Security resources are provisioned,,,,Data Platform,Azure_Terraform,,Design
,,,"1","Execute Terraform apply pipeline","Key Vault exists with expected secrets and access policies",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - Terraform - Client resource group is created,,,,Data Platform,Azure_Terraform,,Design
,,,"1","Create new customer via portal","Client resource group is created and isolated",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - Terraform - Client data resources are created,,,,Data Platform,Azure_Terraform,,Design
,,,"1","Create new customer via portal","Client SQL database Databricks cluster and storage account exist",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - Terraform - Project customer container is created,,,,Data Platform,Azure_Terraform,,Design
,,,"1","Create new project for existing customer","Project customer container is created and linked correctly",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - CI/CD - Code deployment pipeline executes successfully,,,,Data Platform,Code_Deployment_Testing,,Design
,,,"1","Trigger CI/CD deployment pipeline","Pipeline executes all stages without failure",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - CI/CD - Deployed version matches expected build,,,,Data Platform,Code_Deployment_Testing,,Design
,,,"1","Complete deployment","Deployed version matches expected release artifact",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - CI/CD - Smoke test after deployment,,,,Data Platform,Code_Deployment_Testing,,Design
,,,"1","Access deployed portal and API","Portal loads and API responds successfully",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - Security - HITRUST HIPAA pipeline executes successfully,,,,Data Platform,"Azure_Security;HiTrust",,Design
,,,"1","Run HITRUST HIPAA compliance pipeline","Pipeline completes successfully and reports PASS",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - Security - Terraform Checkov scan executes successfully,,,,Data Platform,Azure_Security,,Design
,,,"1","Execute Terraform pipeline","Checkov scan completes with no unresolved critical findings",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - Security - Fortify scan executes successfully,,,,Data Platform,Azure_Security,,Design
,,,"1","Execute web or API deployment pipeline","Fortify SAST scan executes and results are recorded",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - Security - Trivy container scan executes successfully,,,,Data Platform,Azure_Security,,Design
,,,"1","Execute container deployment pipeline","Trivy scan executes with no critical vulnerabilities",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Azure - Security - Azure policy compliance check passes,,,,Data Platform,Azure_Security,,Design
,,,"1","Execute customer infrastructure pipeline","Azure policy compliance check passes",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Security - RBAC - Admin has full portal access,,,,Data Platform,Access_Control,,Design
,,,"1","Login as Admin user","Admin can access all portal functionality",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Security - RBAC - User access restrictions enforced,,,,Data Platform,Access_Control,,Design
,,,"1","Login as User role","Restricted actions are not permitted",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Security - RBAC - Customer has no portal access,,,,Data Platform,Access_Control,,Design
,,,"1","Login as Customer role","Access to operational portal is denied",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Security - RBAC - Restricted UI elements are hidden,,,,Data Platform,Access_Control,,Design
,,,"1","Login as non admin user","Restricted UI elements are not visible",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Post Deployment - Infrastructure - Resources exist,,,,Data Platform,Post_Deployment_Smoke,,Design
,,,"1","Review production environment","Required infrastructure exists",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Post Deployment - Security - Compliance checks pass,,,,Data Platform,Post_Deployment_Smoke,,Design
,,,"1","Review post deployment security pipelines","All security checks completed successfully",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Post Deployment - Smoke - Application is operational,,,,Data Platform,Post_Deployment_Smoke,,Design
,,,"1","Access production portal","Application is accessible with no blocking issues",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Performance - File upload - Large file uploads within acceptable timeframe,,,,Data Platform,Performance_Baseline,,Design
,,,"1","Upload large benchmark dataset","Upload completes within acceptable timeframe",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Performance - Ingestion - Pipeline completes within benchmark,,,,Data Platform,Performance_Baseline,,Design
,,,"1","Run ingestion pipeline with benchmark data","Pipeline runtime meets or improves baseline",,,,
,,,,,,,,,
,,,,,,,,,

,Test Case,Performance - Stability - No failures under large data load,,,,Data Platform,Performance_Baseline,,Design
,,,"1","Run ingestion under heavy load","Pipeline completes without failures or resource exhaustion",,,,
,,,,,,,,,
,,,,,,,,,
