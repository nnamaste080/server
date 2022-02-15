import os
import sqlite3
import random

class FileOperations:

	def __init__(self):
		self.conn = sqlite3.connect('mydb.db')
		self.cursor_obj = self.conn.cursor()
		try:
			self.create_table()
		except sqlite3.OperationalError:
			pass

	#----------lists all files in directory--------------

	def get_all_filenames(self):
		path = 'wordlists'
		return [path+'/'+i for i in list(os.walk(path))[0][2]]
	
	#-------check file availability-------------
	def exists_in_filesystem(self,flask_app_init,filepath):
		return os.path.exists(os.path.join(flask_app_init.root_path,filepath))

	#----------Database---------------

	def create_table(self):
		cmd = 'create table jobs(filepath varchar(255) NOT NULL UNIQUE,status varchar(255),assigned varchar(255))'
		self.cursor_obj.execute(cmd)
		self.conn.commit()

	def set_file_process_completed(self,filename,pcname):
		cmd = f"""insert into jobs(filepath,status,assigned)values('{filename}','completed','{pcname}')"""
		self.cursor_obj.execute(cmd)
		self.conn.commit()
	
	def set_file_process_running(self,filename,pcname):
		cmd = f"""insert into jobs(filepath,status,assigned)values('{filename}','running','{pcname}')"""
		self.cursor_obj.execute(cmd)
		self.conn.commit()
	

	def update_file_process_running(self,filepath,pcname):
		cmd = f"""update jobs set status='running',assigned='{pcname}' where filepath='{filepath}'"""
		self.cursor_obj.execute(cmd)
		self.conn.commit()
	
	def set_file_process_failed(self,filepath):
		cmd = f"""update jobs set status='failed',assigned='' where filepath='{filepath}'"""
		self.cursor_obj.execute(cmd)
		self.conn.commit()	

	def set_file_process_completed_by_workername(self,workername):
		cmd = f"""update jobs set status='completed',assigned='' where assigned='{workername}' and status='running'"""
		self.cursor_obj.execute(cmd)
		self.conn.commit()

	def set_file_process_failed_by_workername(self,workername):
		cmd = f"""update jobs set status='failed',assigned='' where assigned='{workername}' and status='running'"""
		self.cursor_obj.execute(cmd)
		self.conn.commit()		

	#----get failed file where not assigned to anyone------
	def get_failed_files(self):
		cmd = f"""select * from jobs where status='failed' and LENGTH(assigned)=0"""
		self.cursor_obj.execute(cmd)
		data = self.cursor_obj.fetchall()
		return list(data)

	def exists_in_database(self,filepath):
		cmd=f"""select * from jobs where filepath='{filepath}'"""
		self.cursor_obj.execute(cmd)
		data = self.cursor_obj.fetchall()
		return True if len(list(data))>0 else False

	def get_all_files_info(self):
		cmd = """select * from jobs"""
		self.cursor_obj.execute(cmd)
		data = self.cursor_obj.fetchall()
		return list(data)

	def close_conn(self):
		self.conn.close()

class CrackingStatus:
	def __init__(self):
		self.conn = sqlite3.connect('mydb.db')
		self.cursor_obj = self.conn.cursor()
		try:
			self.create_table()
			self.insert()
		except sqlite3.OperationalError:
			pass

	def create_table(self):
		cmd = 'create table CrackingStatus(status varchar(255))'
		self.cursor_obj.execute(cmd)
		self.conn.commit()

	def insert(self):
		cmd = 'insert into crackingstatus(status)values("failed");'
		self.cursor_obj.execute(cmd)
		self.conn.commit()

	def update(self,status):
		cmd = f"""update CrackingStatus set status='{status}';"""
		self.cursor_obj.execute(cmd)
		self.conn.commit()

	def get_status(self):
		cmd = """select * from crackingstatus"""
		self.cursor_obj.execute(cmd)
		data = self.cursor_obj.fetchall()
		return list(data)[0][0]

	def close_conn(self):
		self.conn.close()
