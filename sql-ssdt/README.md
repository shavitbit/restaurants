# SSDT 
SQL Server Data Tools (SSDT) is an integrated development environment (IDE) provided by Microsoft for managing and developing SQL Server databases. SSDT is built into Visual Studio, allowing developers to create, design, and deploy databases, database-related projects, and business intelligence solutions.


# Here’s how it works
In the DevOps CI/CD aspect, SQL Server Data Tools (SSDT) integrates seamlessly to manage and automate database deployments. Here’s how it works:

1. Version Control Integration
Source Control: Store your SSDT database project in a version control system (e.g., Git).
Tracking Changes: Track changes to database schemas and scripts in the same way you manage application code.
2. Build Automation
Build Pipelines: Set up CI pipelines in tools like Azure DevOps to automatically build the SSDT project.
DACPAC Generation: The build process generates a DACPAC file, a package containing the database schema.
3. Testing
Automated Tests: Incorporate unit tests and integration tests for database objects into the CI pipeline to validate changes.
4. Deployment Automation
Release Pipelines: Use CD pipelines to deploy the DACPAC file to target SQL Server instances.
Incremental Deployment: SSDT ensures incremental deployment, applying only the changes necessary to update the target database to match the DACPAC.
5. Rollback and Rollforward
Versioned Releases: Manage rollbacks by keeping track of previous DACPAC versions.
Deployment Scripts: Automatically generated deployment scripts can be reviewed and adjusted as needed.
6. Configuration Management
Environment Configuration: Use variables and configuration files to manage environment-specific settings (e.g., connection strings, database names).
Summary
SSDT in DevOps CI/CD provides a robust framework for automating database deployments, ensuring consistency, and integrating database changes seamlessly with application deployments. This integration supports continuous integration and continuous delivery practices, enhancing the overall 

# instructions
- the table schema location: /sqlproject/DatabaseProjectrestaurantdb/dbo 
- post deployment script location: /sqlproject/DatabaseProjectrestaurantdb/script

- In the SSDT build (ci) the sqlproj,the schema of the tables and the post deployment script will compile and produce a DACPAC file.
<br/>
- In the release pipeline the DACPAC file will be deploy to azure sql server and will sync the schema change if there is one
<br />
- The post deployment script will execute without sync so beware of duplications.
### When you want to insert more record, clean the PostDeploymentScript.sql and fill it with your records.
# Change the SQL password in the SSDT release - every time you apply the terraform a new password generated randomly. 