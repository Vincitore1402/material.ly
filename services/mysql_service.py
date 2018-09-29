import MySQLdb
import MySQLdb.cursors
import sys

sys.path.append('./config')
import config
sys.path.remove('./config')

def getConnection():
	conn = MySQLdb.connect(host=config.DB_HOST, user=config.DB_USER, passwd=config.DB_PASSWORD, db=config.DB_NAME,charset=config.DEFAULT_CHARSET,cursorclass=MySQLdb.cursors.DictCursor)
	return conn