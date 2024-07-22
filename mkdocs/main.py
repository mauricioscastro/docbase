import os
from easydict import EasyDict as edict 
import logging
import psycopg2
import json  
from datetime import datetime

logger = logging.getLogger("hcr.macros")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def define_env(env):

    def postgres_connection():
      try:
        conn = edict(env.variables.sql['connection'])
        logger.debug("connection: " + json.dumps(conn))
        try:
          conn.host = os.environ['DUMPDB_HOST']
          logger.debug("connection host from env: " + conn.host)
        except Exception as e:
          pass
        os.environ()
        return psycopg2.connect(dbname=conn.dbname, user=conn.user, password=conn.password, host=conn.host, port=conn.port)
      except Exception as e:
        logger.error(e)
      return None

    @env.macro
    def doc_env():
      return {name:getattr(env, name) for name in dir(env) if not name.startswith('_')}  

    @env.macro
    def queryddb(query):
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
    def queryddb_mdtable(query):
        logger.debug("queryddb_mdtable query: " + query)
        conn = postgres_connection()
        try:
          with conn:
            with conn.cursor() as cur:
              cur.execute("select * from version")
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

# def on_pre_page_macros(env):
#   print("+++")
#   print(env.page)
#   print(env.conf.extra['alternate'])
  
  # print(env.variables.alternate)  
  # env.conf['pdf_present'] = os.path.exists(env.conf.site_dir + "/site.pdf")
  # print(env.conf['pdf_present'])
  # print(env.markdown)
  # env.variables.extra['site_dir'] = env.conf.site_dir
  # logger.info(env.conf.site_dir)
    # print("+++")
    # alternate = None
    # try:
    #     alternate = env.variables.alternate
    # except:
    #     pass
    # print(alternate)  
    # print("+++")
    # print(env.variables.author)
    # print("+++")
    # print(env.page)
    # print("+++")  
    # print(env.config)
    # print("+++")    
    # print(env.conf.plugins['i18n'])
    # print("+++")       
    # print(json.dumps(env.conf.plugins, indent=2))
    # print("+++")        


# def on_post_page_macros(env):
#     "After macros were executed"
#     # This will add a (Markdown or HTML) footer
#     # footer = '\n'.join(
#     #     ['', '##Added Footer (Post-macro)', 'Name of the page is _%s_' % env.page.title])
#     # env.markdown += footer
#     print("+++")
#     print(env.markdown)
#     print("+++")