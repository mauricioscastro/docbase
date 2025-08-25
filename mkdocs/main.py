import os
from easydict import EasyDict as edict 
import logging
import psycopg2
import json  
from datetime import datetime
import base64

logger = logging.getLogger("hcr.macros")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def define_env(env):

    env.variables['hide_secondary_side_bar'] = "<script>document.getElementsByClassName('md-sidebar--secondary')[0].style.display = 'none';</script>"

    def base64(filepath):
      try:
          with open(filepath, 'rb') as file:
              encoded_content = base64.b64encode(file.read())
              return encoded_content.decode('utf-8')
      except Exception as e:
          logger.error(e)   
      return ""

    def postgres_connection():
      try:
        conn = edict(env.variables.sql['connection'])
        logger.debug("connection: " + json.dumps(conn))
        try:
          conn.host = os.environ['DUMPDB_HOST']
          logger.debug("connection host from env: " + conn.host)
        except Exception as e:
          pass
        return psycopg2.connect(dbname=conn.dbname, user=conn.user, password=conn.password, host=conn.host, port=conn.port)
      except Exception as e:
        logger.error(e)
      return None

    @env.macro
    def doc_env():
      return {name:getattr(env, name) for name in dir(env) if not name.startswith('_')}  

    @env.macro
    def querydb(query):
        logger.debug("queryddb query: " + query)
        conn = postgres_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    return cur.fetchall()
        except Exception as e:          
          logger.error(e)          
        finally:
          if conn: conn.close()
        return ()

    @env.macro
    def querydb_mdtable(query):
        logger.debug("queryddb_mdtable query: " + query)
        conn = postgres_connection()
        try:
          with conn:
            with conn.cursor() as cur:
              cur.execute(query)
              column_descriptions = cur.description
              column_names = [desc[0] for desc in column_descriptions]
              data_rows = cur.fetchall()
              header_row = "| " + " | ".join(column_names) + " |"
              separator_row = "| -" + (" | -" * (len(column_names)-1)) + " |"
              data_rows_markdown = []
              for row in data_rows:
                escaped_row = [str(x).replace("|", "\\|") for x in row]
                data_rows_markdown.append("| " + " | ".join(escaped_row) + " |")
              table = "\n".join([header_row, separator_row] + data_rows_markdown)
              return table
        except Exception as e:          
          logger.error(e)         
        finally:
          if conn: conn.close()
        return ""

