import psycopg2
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import DS_Generated_Review_Final

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

        DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        self.engine = create_engine(DATABASE_URL, echo=False, future=True)

        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, future=True)


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

    def get_vulnerability_commits(self, generated: bool = True, limit: int = 0) -> list[dict]:
        """
        Retrieve vulnerability-fixing commits from the database.

        Args:
            generated (bool): If True, include those already generated.
            limit (int): The maximum number of commits to retrieve (0 for no limit).

        Returns:
            list[dict]: A list of vulnerability-fixing commit information.
        """
        query = "SELECT sha, message, patch FROM ds_generated_review_final WHERE usable = true"
        if not generated:
            query += " and review is null"
        
        if limit > 0:
            query += f" LIMIT {limit}"
        
        self.cur.execute(query)
        results = self.cur.fetchall()

        commits = []
        for result in results:
            commits.append({
                "sha": result[0],
                "message": result[1],
                "patch": result[2]
            })

        return commits
    
    def save_generated_code_review(self, sha: str, code_review: str):
        """
        Save the generated code review for a given commit SHA.

        Args:
            sha (str): The commit SHA.
            code_review (str): The generated code review.
        """
        with self.SessionLocal() as session:
            existing_entry = session.query(DS_Generated_Review_Final).filter_by(sha=sha).first()
            if existing_entry:
                existing_entry.review = code_review
                session.commit()