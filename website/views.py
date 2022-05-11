from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from website.extensions import db
from website.models import (User, Ranking, UnknowRegion, Cluster, Region, 
                        SkippedRanking, NeighbouringRegion) 

import random
import numpy as np
import uuid

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
 organisation = SelectField('Which type of organisation do you work for?', choices=[('g', 'governmental'), ('ng','non-governmental')], validators=[DataRequired()])
 work_field = SelectField('What is primarily your client base?', choices=[('sw','sex workers'),('ms', 'modern slavery/human trafficking victims'), \
     ('s', 'survivors'), ('m', 'multiple'), ('o','other')], validators=[DataRequired()])

blueprint = Blueprint('views', __name__)

@blueprint.route('/')
def intro():
    session.clear()
    return render_template('ethics_approval.html')

@blueprint.route('/introduction')
def introduction():
    return render_template('introduction.html')


@blueprint.route('/rank')
@blueprint.route('/rank/<rid1>/<rid2>')
def rank(rid1=None, rid2=None):

    region_id = 0
    cluster_id = 1

    first_region = random.choice(session['user_region_bucket'])

    r1_id = first_region[region_id]
    sublist = [region for region in session['user_region_bucket'] if region[cluster_id] == first_region[cluster_id]] 
    sublist.remove(first_region)
    r2_id = random.choice(sublist)[region_id]

    r1 = Region.query.filter_by(id=r1_id).first()
    r2 = Region.query.filter_by(id=r2_id).first()

    return render_template('ranking_interface.html', r1=r1, r2=r2)


@blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    session.clear()
    if request.method == 'POST':     

        session['known'] = list(request.form)
        session['known'].remove('work_field')
        session['known'].remove('organisation')


        uk_clusters = {'NE': 1, 'NW': 2, 'Y&H': 3, 'EM': 4, 'WM': 5, 'East': 6, 'L': 7, 'SE': 8, 'SW': 9}
        
        ne, nw, yh, em, wm, east, l, se, sw = [True if cluster in session['known'] else False for cluster in uk_clusters]
        
        organisation = request.form['organisation']
        work_field = request.form['work_field']

        user = User(ne=ne, nw=nw, yh=yh, em=em, wm=wm, east=east, l=l, se=se, sw=sw, organisation=organisation, work_field=work_field)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        
        session['user_region_bucket'] = []
        for cluster_name in session['known']:
            relevant_regions = Region.query.filter_by(cluster_id=uk_clusters[cluster_name]).all()            
            session['user_region_bucket'].extend([(region.id, region.cluster_id) for region in relevant_regions])

            neighbouring_regions = NeighbouringRegion.query.filter_by(cluster_id=uk_clusters[cluster_name]).all()
            session['user_region_bucket'].extend([(n_region.region_id, n_region.cluster_id) for n_region in neighbouring_regions])

        return redirect(url_for('.rank'))

    user_form = UserForm()
    return render_template('entire_map.html', form=user_form)


@blueprint.route('/store')
@blueprint.route('/store/<lesser>/<greater>')
def store_ranking(lesser=None, greater=None):
    r = Ranking(user_id=session['user_id'], lesser=lesser, greater=greater)

    db.session.add(r)
    db.session.commit()

    return redirect(url_for('.rank'))


@blueprint.route('/skip/<r1>/<r2>')
def skip_ranking(r1=None, r2=None):
    s = SkippedRanking(user_id=session['user_id'], r1=r1, r2=r2)

    db.session.add(s)
    db.session.commit()

    return redirect(url_for('.rank'))


@blueprint.route('/previous')
def previous_ranking():
    r = Ranking.query.filter_by(user_id=session['user_id']).order_by(
        Ranking.date.desc()).first()

    r.rejudged = True

    db.session.add(r)
    db.session.commit()

    r1 = Region.query.filter_by(id=r.lesser).first()
    r2 = Region.query.filter_by(id=r.greater).first()

    return render_template('ranking_interface.html', r1=r1, r2=r2)


@blueprint.route('/unknown/<swid>/<cwid>')
def store_unknown_region(swid, cwid):
    u = UnknowRegion(user_id=session['user_id'], region_id=swid)

    ks = session['user_region_bucket']
    session['user_region_bucket'] = [region for region in ks if region[0]!=int(swid)]

    db.session.add(u)
    db.session.commit()

    return redirect(url_for('.rank'))


@blueprint.route('/logout')
def logout():
    print(session.keys())
    session.clear()
    print(session.keys())
    return render_template('final.html')
