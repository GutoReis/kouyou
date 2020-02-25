kouyou.google package
=====================

To use the google package from kouyou, it's needed to create a .env file with the following keys on it:

| *export GOOGLE_PROJECT_ID="SAMPLE_ID"*
| *export GOOGLE_PRIVATE_KEY_ID="SAMPLE_KEY_ID"*
| *export GOOGLE_PRIVATE_KEY="SAMPLE_KEY"*
| *export GOOGLE_CLIENT_EMAIL="SAMPLE_CLIENT_EMAIL"*
| *export GOOGLE_CLIENT_ID="SAMPLE_CLIENT_ID"*
| *export GOOGLE_CLIENT_X509_CERT_URL="SAMPLE_CLIENT_X509_CERT_URL"*

.. note:: In order to have **GOOGLE variables** to use in the ``.env`` file, you must create a project in the `Google Cloud Platform <https://console.cloud.google.com/home/>`__ or use an existing one. Inside the project, go to `credential <https://console.cloud.google.com/apis/credentials>`__ select **+ Create Credential** and choose **Service Account**. Then it will generate a file with the credentials values, download it.

.. warning:: The ``.env`` file must be in the root of the project directory, so the dotenv package can still find it.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   kouyou.google.drive
   kouyou.google.sheets
