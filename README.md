python-cydia-repo-updater
=========================

**Patchwork Python script that should cover a basic Cydia repo's automated needs**

The main script, updaterepo.py, is meant to be run with superuser privilidges in the root directory of the repo.

The script includes a feature to handle new packages. In the repo root directory, a directory can be created for the purpose of holding new packages that have yet to be uploaded. These new packages can be in either a packaged .deb format already, or a series of dictories (with DEBIAN/control) waiting to be packaged.
The purpose of this new packages feature is to limit uploads to only new (or updated) packages.

In the updaterepo.py file,
* /REPODIRECTORY should be replaced with the path to the root directory of the repo
* /REPODIRECTORY/new should be replaced with the path to the directory inside the repo root that contains new packages
* GPGSIGNATUREID (line 47) should be replaced with the signature ID used to sign the Release file
* GPGSIGNATUREPASSWORD (line 47) should be replaced with the passphrase for the signature ID used to sign the Release file
* FTPADDRESS (line 55) should be replaced with the address of the FTP server to be uploaded to
* FTPUSERNAME (line 55) should be replaced with the login username of the FTP server to be uploaded to
* FTPPASSWORD (line 55) should be replaced with the password to the login username of the FTP server to be uploaded to
* /FTPUPLOADDIRECTORY/ (line 56) should be replaced with the path of the directory to upload to on the FTP server
