from website.extensions import db
import datetime


class Cluster(db.Model):
    __tablename__ = 'clusters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    #cluster = db.Column(db.Integer, nullable=False)

class Region(db.Model):
    __tablename__ = 'regions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    shapefile_id = db.Column(db.String(255), nullable=False)
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id'), nullable=False)

    cluster = db.relationship('Cluster', backref=db.backref('regions', lazy=True))

class NeighbouringRegion(db.Model):
    __tablename__ = 'neighbours'

    id = db.Column(db.Integer, primary_key=True)
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id'), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)

    cluster = db.relationship('Cluster', backref=db.backref('clusters', lazy=True))
    region = db.relationship('Region', backref=db.backref('regions', lazy=True))

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    ne = db.Column(db.Boolean(), default=False)
    nw = db.Column(db.Boolean(), default=False)
    yh = db.Column(db.Boolean(), default=False)
    em = db.Column(db.Boolean(), default=False)
    wm = db.Column(db.Boolean(), default=False)
    east = db.Column(db.Boolean(), default=False)
    l = db.Column(db.Boolean(), default=False)
    se = db.Column(db.Boolean(), default=False)
    sw = db.Column(db.Boolean(), default=False)
    work_field = db.Column(db.String(2), default=False)
    organisation = db.Column(db.String(2), default=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<User %d>' % (self.id)


class Ranking(db.Model):
    __tablename__ = 'comparisons'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    lesser = db.Column(
        db.Integer, db.ForeignKey('regions.id'), nullable=False)
    greater = db.Column(
        db.Integer, db.ForeignKey('regions.id'), nullable=False)
    rejudged = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('rankings', lazy=True))

    def __repr__(self):
        return '<Ranking {} {} lesser {} greater {}>'.format(
            self.date, self.user_id, self.lesser, self.greater)


class SameRanking(db.Model):
    __tablename__ = 'same_rankings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    r1 = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)
    r2 = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('same_rankings', lazy=True))


class UnknowRegion(db.Model):
    __tablename__ = 'user_unknown_regions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    region_id = db.Column(
        db.Integer, db.ForeignKey('regions.id'), nullable=False)

    user = db.relationship(
        'User', backref=db.backref('unknown_regions', lazy=True))
    region = db.relationship(
        'Region', backref=db.backref('unknown_by_users', lazy=True))

  