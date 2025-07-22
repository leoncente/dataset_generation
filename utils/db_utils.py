import psycopg2
import random

class DatabaseConnection:
    def __init__(self, db_host: str, db_user: str, db_password: str, db_port: int, db_name: str):
        # Connect to the PostgreSQL database
        self.conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            port=db_port,
            database=db_name
        )

        # Create a cursor object
        self.cur = self.conn.cursor()

    def get_vulnerability_fixes(self, version: str) -> list[str]:
        """
        Retrieve vulnerability-fixing commits from the database for the given version.
        Returns a list of commit SHAs.
        """
        query = (
            "SELECT sha FROM ds_eval "
            "WHERE security IS NOT NULL "
            "GROUP BY sha "
            "HAVING COUNT(*) = 2 AND SUM(CASE WHEN security THEN 1 ELSE 0 END) = 2 "
            "UNION "
            "SELECT sha FROM ds_discrepancies "
            "WHERE security = true"
        )


        self.cur.execute(query)
        results = self.cur.fetchall()
        
        shas = [result[0] for result in results]
        
        random.shuffle(shas)

        return shas
    
    def get_commit_info(self, sha: str) -> dict:
        """
        Retrieve commit details from the database for the given SHA.
        Returns a dictionary with commit details.
        """
        query = "SELECT owner, name FROM ds_commit WHERE sha = %s"
        self.cur.execute(query, (sha,))
        result = self.cur.fetchone()
        
        if result:
            return {
                "owner": result[0],
                "name": result[1]
            }
        
        return {}
