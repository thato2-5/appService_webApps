Azure Flask Web Apps
Description

This repository contains the source code for a Python Flask web application deployed on Microsoft Azure. The project aims to provide a scalable and robust web application framework, leveraging the powerful features of Azure for hosting and management. The repository includes all necessary configuration files, deployment scripts, and sample applications to get started quickly.

Features

  * Python Flask Framework: Utilizes the lightweight and flexible Flask framework for web development.
  * Azure Integration: Seamless integration with Azure services for deployment, scaling, and monitoring.
  * Containerization: Docker support for containerized applications, ensuring consistency across development, testing, and production environments.
  * Continuous Integration/Continuous Deployment (CI/CD): Automated pipelines for building, testing, and deploying the application.
  * Sample Applications: Includes example Flask applications to demonstrate common patterns and best practices.
  * Extensive Documentation: Detailed instructions and guides for setting up and running the application both locally and on Azure.

Getting Started
Prerequisites

  * Python 3.x
  * Azure CLI
  * Docker (optional, for containerized deployments)
  * Git

Installation

  Clone the repository:

    git clone https://github.com/thato2-5/appService_webApps.git
    cd appService_webApps

Create and activate a virtual environment:

    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install dependencies:

    pip install -r requirements.txt

Run the application locally:

    flask run

Deployment
Deploy to Azure App Service

  Login to Azure:

    az login

Create a resource group:

    az group create --name myResourceGroup --location southafricanorth

Create an App Service plan:

    az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku FREE

Create a web app:

    az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myUniqueAppName --runtime "PYTHON|3.8"

Deploy the application:

    az webapp up --name myUniqueAppName --resource-group myResourceGroup

#### Screenshots / Video Demo:
** Screenshot 1:** [First Form]
![Image](https://github.com/thato2-5/appService_webApps/blob/Blog/blob_visualizer.png)

** Screenshot 1:** [First Form]
![Image](https://github.com/thato2-5/appService_webApps/blob/Blog/blog_home.png)


** Screenshot 1:** [First Form]
![Image](https://github.com/thato2-5/appService_webApps/blob/Blog/blog_home.png)


** Screenshot 1:** [First Form]
![Image](https://github.com/thato2-5/appService_webApps/blob/Blog/blog_home.png)


** Screenshot 1:** [First Form]
![Image](https://github.com/thato2-5/appService_webApps/blob/Blog/blog_home.png)


** Screenshot 1:** [First Form]
![Image](https://github.com/thato2-5/appService_webApps/blob/Blog/blob_signin.png)

** Screenshot 1:** [First Form]
![Image](https://github.com/thato2-5/appService_webApps/blob/Blog/blob_subscribe.png)

Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.
License

This project is licensed under the MIT License.
Acknowledgments

    Flask Documentation: https://flask.palletsprojects.com/
    Azure Documentation: https://docs.microsoft.com/en-us/azure/
