from os import system as s # s will serve as an easy way to send a command to the system
from os import path, remove, listdir
import hashlib, shutil, ftplib, gnupg

news = listdir('/REPODIRECTORY/new') # Taking inventory of all new packages, placed in a "/new" directory
for entry in news:
	enpath = '/REPODIRECTORY/new/%s' % entry
	if path.isdir(enpath): # Checking to see if any packages (in directory form, with the DEBIAN directory) have yet to be packaged
		makedeb = 'dpkg -b %s' % enpath
		s(makedeb) # Packaging any not-yet-packaged packages
		shutil.rmtree(enpath) # Deleting the now-packaged package's folder

news = listdir('/REPODIRECTORY/new') # Taking inventory of all new packages
for file in news:
	newf = path.join('/REPODIRECTORY/new', file)
	newfm = path.join('/REPODIRECTORY', file)
	shutil.move(newf, newfm) # Moving all new packages into the repo root, so they can be accounted for when creating the Packages index

remove('Packages') # Removing the old Packages index files
remove('Packages.gz')
remove('Packages.bz2')

s('sudo dpkg-scanpackages -m . /dev/null >Packages') # Creating the Pacakges file
s('bzip2 -fks Packages') # Creating the Packages.bz2 file
s('gzip -f Packages') # Turning the Packages file into the Packages.gz file
s('sudo dpkg-scanpackages -m . /dev/null >Packages') # Creating another Packages file

m1 = hashlib.md5(open('Packages').read()).hexdigest() # Calculating checksums for each Packages index file
m2 = hashlib.md5(open('Packages.gz').read()).hexdigest()
m3 = hashlib.md5(open('Packages.bz2').read()).hexdigest()

s1 = path.getsize('Packages') # Getting file size of each Packages index files
s2 = path.getsize('Packages.gz')
s3 = path.getsize('Packages.bz2')

sums = '%s %s Packages\n%s %s Packages.gz\n%s %s Packages.bz2\n' % (m1, s1, m2, s2, m3, s3)
with open("Release", "r+") as f: # Writing the sums & file sizes of the Packages index files to the Release file
	old = f.read()
	old = old[:XXX] ### This XXX varies on how long the Release file is, as this line skips to the end of the Release file to tag on the sums
	f.seek(0)
	f.write(old + sums)


gpg = gnupg.GPG()

nosign = open('Release', "rb") # Signing the Release file
signed = gpg.sign_file(nosign, keyid='GPGSIGNATUREID', passphrase='GPGSIGNATUREPASSWORD')

remove('Release.gpg') # Removing the old Release.gpg signed file

open("Release.gpg", "w").write(str(signed)[XXX:]) # Create and write signature data to Release.gpg
# On the line above, the XXX varies on how long the Release file is, as gpg.sign_file from 5 lines up outputs more than Cydia wants


session = ftplib.FTP('FTPADDRESS','FTPUSERNAME','FTPPASSWORD') # Setting up a FTP connection
ftplib.FTP.cwd(session,'/FTPUPLOADDIRECTORY/')

news.append('Packages') # Preparing files for upload (only new packages, and the index files)
news.append('Packages.gz')
news.append('Packages.bz2')
news.append('Release')
news.append('Release.gpg')

for file in news: # Upload each file, and print as each file is uploaded
	upl = open(file, 'rb')
	upcmd = 'STOR %s' % file
	session.storbinary(upcmd, upl)
	print '%s uploaded.' % file
	upl.close()

print 'Finished uploads.'
