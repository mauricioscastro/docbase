import os
from easydict import EasyDict as edict 
import logging
import psycopg2
import json  
from datetime import datetime
import base64
from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS
from diagrams.aws.database import ElastiCache, RDS
from diagrams.aws.network import ELB
from diagrams.aws.network import Route53

logger = logging.getLogger("hcr.macros")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def generate_base64_pdf_cover(filepath="withpdf/cover_img.png", destination="withpdf/cover.png.b64"):
  try:
      with open(filepath, 'rb') as file:
          encoded_content = base64.b64encode(file.read())
          with open(destination, 'wb') as dest_file:
            dest_file.write(encoded_content)
  except Exception as e:
      logger.error(e)   

def postgres_connection(env):
  try:
    conn = edict(env.variables.sql['connection'])
    logger.debug("connection: " + json.dumps(conn))
    try:
      conn.host = os.environ['DUMPDB_HOST']
      logger.debug("connection host from env: " + conn.host)
    except Exception as e:
      logger.info("env var not found or unused: " + str(e))
      pass
    return psycopg2.connect(dbname=conn.dbname, user=conn.user, password=conn.password, host=conn.host, port=conn.port)
  except Exception as e:
    logger.error(e)
  return None

def generate_diagram():
    with Diagram("Current Architecture", 
                 filename="docs/img/architecture", 
                 graph_attr={"bgcolor": "transparent", "fontcolor": "#9F76C1"}, 
                 node_attr={"fontcolor": "#9F76C1"}, 
                 show=False):
        dns = Route53("DNS")
        lb = ELB("Load Balancer")
        db = RDS("Database")
        cache = ElastiCache("Cache")
        ecs = ECS("ECS Cluster")

        dns >> lb >> ecs
        ecs >> db
        ecs >> cache

def define_env(env):

    env.conf['extra']['client'] = env.variables.hcr.get('client', 'Client') 
    env.conf['extra']['authors'] = env.variables.hcr.get('authors', 'John Doe, Jane Doe')

    if env.conf['extra'].get('site_build_date') == "1970-01-01":
      env.conf['extra']['site_build_date'] = datetime.now().strftime("%Y-%m-%d")

    if isinstance(env.conf['extra']['authors'], str):
      env.conf['extra']['authors'] = env.conf['extra']['authors'].split(',')

    env.variables['hide_secondary_side_bar'] = "<script>document.getElementsByClassName('md-sidebar--secondary')[0].style.display = 'none';</script>"

    generate_diagram()
    generate_base64_pdf_cover()

    @env.macro
    def doc_env():
      return {name:getattr(env, name) for name in dir(env) if not name.startswith('_')}  

    @env.macro
    def querydb(query):
        logger.debug("queryddb query: " + query)
        conn = postgres_connection(env)
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
        conn = postgres_connection(env)
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

