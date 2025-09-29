from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text, BigInteger
from sqlalchemy.schema import PrimaryKeyConstraint, ForeignKeyConstraint


class Base(DeclarativeBase):
    pass

class Repo(Base):
    __tablename__ = 'repo'

    owner = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    mined = Column(Boolean, default=False)
    prs = relationship('PR', backref='repo')

    __table_args__= (
        PrimaryKeyConstraint('owner', 'name'),
    )

class PR(Base):
    __tablename__ = 'pr'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    state = Column(String)
    merged = Column(Boolean)
    created_at = Column(String)
    merged_at = Column(String)
    author = Column(String)
    author_type = Column(String)
    comments_num = Column(Integer)
    review_comments = Column(Integer)
    commits_num = Column(Integer)
    changed_files = Column(Integer)
    owner = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    mined = Column(Boolean, default=False)
    commits = relationship('Commit', backref='pr')
    comments = relationship('Comment', backref='pr')
    reviews = relationship('Review', backref='pr')

    __table_args__= (
        ForeignKeyConstraint(['owner', 'name'], ['repo.owner', 'repo.name']),
        PrimaryKeyConstraint('id', 'owner', 'name'),
    )

class Commit(Base):
    __tablename__ = 'commit'

    sha = Column(String, primary_key=True)
    author = Column(String)
    author_email = Column(String)
    message = Column(String)
    date = Column(String)
    tree = Column(String)
    pr_id = Column(Integer)
    owner = Column(String)
    name = Column(String)
    files = relationship('File', backref='commit')

    __table_args__= (
        ForeignKeyConstraint(['pr_id', 'owner', 'name'], ['pr.id', 'pr.owner', 'pr.name']),
    )

class File(Base):
    __tablename__ = 'file'

    sha = Column(String, primary_key=True)
    path = Column(String)
    status = Column(String)
    additions = Column(Integer)
    deletions = Column(Integer)
    changes = Column(Integer)
    patch = Column(Text)
    blob_url = Column(String)
    raw_url = Column(String)
    #content = Column(Text)
    commit_sha = Column(String, ForeignKey('commit.sha'))

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(BigInteger, primary_key=True)
    pr_review_id = Column(BigInteger)
    body = Column(String)
    created_at = Column(String)
    author = Column(String)
    author_type = Column(String)
    diff_hunk = Column(Text)
    path = Column(String)
    commit_id = Column(String)
    original_commit_id = Column(String)
    original_line = Column(Integer)
    side = Column(String)
    in_reply_to_id = Column(BigInteger)
    pr_id = Column(Integer)
    owner = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    possible_response = Column(Boolean, default=False)

    __table_args__= (
        ForeignKeyConstraint(['pr_id', 'owner', 'name'], ['pr.id', 'pr.owner', 'pr.name']),
        PrimaryKeyConstraint('id', 'owner', 'name'),
    )

class Review(Base):
    __tablename__ = 'review'

    pr_id = Column(Integer)
    owner = Column(String)
    name = Column(String)
    comment_id = Column(BigInteger, primary_key=True)
    original_commit = Column(String, ForeignKey('commit.sha'), primary_key=True)
    fix_commit = Column(String, ForeignKey('commit.sha'), primary_key=True)
    keywords = Column(Text, default='')
    security = Column(Boolean, default=False)
    review_commits = relationship('Review_Commits', backref='review')

    __table_args__= (
        PrimaryKeyConstraint('comment_id', 'original_commit', 'fix_commit'),
        ForeignKeyConstraint(['pr_id', 'owner', 'name'], ['pr.id', 'pr.owner', 'pr.name']),
        ForeignKeyConstraint(['comment_id', 'owner', 'name'], ['comment.id', 'comment.owner', 'comment.name']),
    )

class User(Base):
    __tablename__ = 'user'

    name = Column(String, primary_key=True)
    password = Column(String)
    token = Column(String)

class Eval(Base):
    __tablename__ = 'eval'

    name = Column(String, ForeignKey('user.name'), primary_key=True)
    comment_id = Column(BigInteger, primary_key=True)
    original_commit = Column(String, primary_key=True)
    fix_commit = Column(String, primary_key=True)
    security = Column(Boolean)
    reason = Column(Text)
    correct = Column(Boolean)
    chosen = Column(Boolean, default=False)
    comment = Column(Text)

    __table_args__= (
        PrimaryKeyConstraint('name', 'comment_id', 'original_commit', 'fix_commit'),
        ForeignKeyConstraint(['comment_id', 'original_commit', 'fix_commit'], ['review.comment_id', 'review.original_commit', 'review.fix_commit']),
    )

class Review_Commits(Base):
    __tablename__ = 'review_commits'

    comment_id = Column(BigInteger, primary_key=True)
    original_commit = Column(String, primary_key=True)
    fix_commit = Column(String, primary_key=True)
    commit_sha = Column(String, primary_key=True)
    owner = Column(String)
    name = Column(String)

    __table_args__= (
        PrimaryKeyConstraint('comment_id', 'original_commit', 'fix_commit', 'commit_sha'),
        ForeignKeyConstraint(['comment_id', 'original_commit', 'fix_commit'], ['review.comment_id', 'review.original_commit', 'review.fix_commit']),
        ForeignKeyConstraint(['commit_sha'], ['commit.sha']),
    )

class Review_differences(Base):
    __tablename__ = 'review_differences'

    comment_id = Column(BigInteger, primary_key=True)
    original_commit = Column(String, primary_key=True)
    fix_commit = Column(String, primary_key=True)
    security = Column(Boolean)
    correct = Column(Boolean)
    comment = Column(Text)
    __table_args__= (
        PrimaryKeyConstraint('comment_id', 'original_commit', 'fix_commit'),
        ForeignKeyConstraint(['comment_id', 'original_commit', 'fix_commit'], ['review.comment_id', 'review.original_commit', 'review.fix_commit']),
    )

class Eval_Model(Base):
    __tablename__ = 'eval_model'

    comment_id = Column(BigInteger, primary_key=True)
    original_commit = Column(String, primary_key=True)
    fix_commit = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    model = Column(String, primary_key=True)
    promt = Column(String, primary_key=True)
    res = Column(String)
    comment = Column(String)
    __table_args__= (
        PrimaryKeyConstraint('comment_id', 'original_commit', 'fix_commit', 'type', 'model', 'promt'),
        ForeignKeyConstraint(['comment_id', 'original_commit', 'fix_commit'], ['review.comment_id', 'review.original_commit', 'review.fix_commit']),
    )

class Eval_Model_Info(Base):
    __tablename__ = 'eval_model_info'

    comment_id = Column(BigInteger, primary_key=True)
    original_commit = Column(String, primary_key=True)
    fix_commit = Column(String, primary_key=True)
    file = Column(String)
    diff = Column(String)
    __table_args__= (
        PrimaryKeyConstraint('comment_id', 'original_commit', 'fix_commit'),
        ForeignKeyConstraint(['comment_id', 'original_commit', 'fix_commit'], ['review.comment_id', 'review.original_commit', 'review.fix_commit']),
    )

## Tables for the commit analysis for the dataset generation

class DS_Commit(Base):
    __tablename__ = 'ds_commit'

    sha = Column(String, primary_key=True)
    author = Column(String)
    author_email = Column(String)
    message = Column(String)
    date = Column(String)
    owner = Column(String)
    name = Column(String)
    file_name = Column(String)
    keywords = Column(String)

class DS_Eval(Base):
    __tablename__ = 'ds_eval'

    name = Column(String, ForeignKey('user.name'), primary_key=True)
    sha = Column(String, ForeignKey('ds_commit.sha'), primary_key=True)
    security = Column(Boolean)
    reason = Column(Text)
    mentions_security = Column(Boolean)
    chosen = Column(Boolean, default=False)
    comment = Column(Text)

    __table_args__= (
        PrimaryKeyConstraint('name', 'sha'),
    )

class DS_Discrepancies(Base):
    __tablename__ = 'ds_discrepancies'

    sha = Column(String, primary_key=True)
    security = Column(Boolean)
    reason = Column(Text)
    mentions_security = Column(Boolean)
    comment = Column(Text)

class DS_Generated_Review(Base):
    __tablename__ = 'ds_generated_review'

    sha = Column(String, ForeignKey('ds_commit.sha'))
    model = Column(String)
    prompt = Column(String)
    review = Column(Text)

    __table_args__= (
        PrimaryKeyConstraint('sha', 'model', 'prompt'),
    )

class DS_Generated_Review_Eval(Base):
    __tablename__ = 'ds_generated_review_eval'

    sha = Column(String, ForeignKey('ds_commit.sha'))
    model = Column(String)
    prompt = Column(String)
    name = Column(String, ForeignKey('user.name'))
    coherent = Column(Boolean)
    vulnerability = Column(Boolean)
    plausible = Column(Boolean)

    __table_args__= (
        PrimaryKeyConstraint('sha', 'model', 'prompt', 'name'),
        ForeignKeyConstraint(['sha', 'model', 'prompt'], ['ds_generated_review.sha', 'ds_generated_review.model', 'ds_generated_review.prompt']),
    )

class DS_Generated_Review_Discrepancy(Base):
    __tablename__ = 'ds_generated_review_discrepancy'

    sha = Column(String, ForeignKey('ds_commit.sha'))
    model = Column(String)
    prompt = Column(String)
    coherent = Column(Boolean)
    vulnerability = Column(Boolean)
    plausible = Column(Boolean)

    __table_args__= (
        PrimaryKeyConstraint('sha', 'model', 'prompt'),
        ForeignKeyConstraint(['sha', 'model', 'prompt'], ['ds_generated_review.sha', 'ds_generated_review.model', 'ds_generated_review.prompt']),
    )
