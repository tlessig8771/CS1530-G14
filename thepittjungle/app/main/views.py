from flask import session, render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, g
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm,\
    CommentForm, RestaurantForm, EventForm, AttractionForm, HikeForm, FilterRestaurant, FilterAttraction
from .. import db
from datetime import datetime
from ..models import Permission, Role, User, Post, Comment, Restaurant, Event, Events, Attraction, Hike
from ..decorators import admin_required, permission_required
import base64
import operator

import app
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    if value is None:
        return ""
    return value.strftime(format)

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           show_followed=show_followed, pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))
    
@main.route('/add_restaurant', methods=['GET','POST'])
@login_required
@admin_required
def add_restaurant():
    form = RestaurantForm()
    if form.validate_on_submit():
        restaurant = Restaurant(restaurant_name=form.name.data,
                                address = form.address.data,
                                phone = form.phone.data,
                                about_me = form.about_me.data,
                                tags = form.tags.data,
                                image = form.file.data.read())
        db.session.add(restaurant)
        db.session.commit()
    return render_template('add_restaurant.html', form=form)

@main.route('/add_attraction', methods=['GET','POST'])
@login_required
def add_attraction():
    form = AttractionForm()
    if form.validate_on_submit():
        attraction = Attraction(attraction_name=form.attraction_name.data,
                                address = form.address.data,
                                phone = form.phone.data,
                                about_me = form.about_me.data,
                                tags = form.tags.data,
                                image = form.file.data.read())
        db.session.add(attraction)
        db.session.commit()
    return render_template('add_attraction.html', form=form)

@main.route('/attractions', methods=['GET', 'POST'])
def show_attractions():
    form = FilterAttraction()
    #if form.validate_on_submit():
    filterAct = form.filterActivity.data
    if(filterAct == 'None'):
        filterAct = 'Show All'
    print(filterAct)
    if current_user.is_authenticated:
        attractions = Attraction.query.all()

        print("ACT TAGS")
        print(current_user.hiking)
        print(current_user.extreme_sports)
        print(current_user.kayaking)
        print(current_user.nature)
        print(current_user.movies)
        print(current_user.sports)
        print(current_user.concerts)
        print(current_user.art_history)
        print(current_user.science_tech)
        print(current_user.entertainment)

        current_user.nature = current_user.nature + 1
        current_user.hiking = current_user.hiking + 1
        current_user.kayaking = current_user.kayaking + 1
        current_user.extreme_sports = current_user.extreme_sports + 1
        current_user.sports = current_user.sports + 1
        current_user.movies = current_user.movies + 1
        current_user.concerts = current_user.concerts + 1
        current_user.art_history = current_user.art_history + 1
        current_user.science_tech = current_user.science_tech + 1
        current_user.entertainment = current_user.entertainment + 1
        db.session.commit()
        
        print("ACT TAGS")
        print(current_user.hiking)
        print(current_user.extreme_sports)
        print(current_user.kayaking)
        print(current_user.nature)
        print(current_user.movies)
        print(current_user.sports)
        print(current_user.concerts)
        print(current_user.art_history)
        print(current_user.science_tech)
        print(current_user.entertainment)
        
        return render_template('attractions.html', attractions=attractions, base64=base64, form=form, filterAct=filterAct)
    return redirect('login.html')   

@main.route('/add_hike', methods=['GET','POST'])
@login_required
def add_hike():
    form = HikeForm()
    if form.validate_on_submit():
        hike = Hike(hike_name=form.hike_name.data,
                    trail_head = form.address.data,
                    about_me = form.about_me.data,
                    tags = form.tags.data,
                    image = form.file.data.read())
        db.session.add(hike)
        db.session.commit()
    return render_template('add_hike.html', form=form)

@main.route('/hike')
def show_hikes():
    hikes = Hike.query.all()    
    return render_template('hikes.html', hikes=hikes, base64=base64)

@main.route('/restaurants', methods=['GET', 'POST'])
def show_restaurants():
    form = FilterRestaurant()
    #if form.validate_on_submit():
    filterRest = form.filterRestaurant.data
    if(filterRest == 'None'):
        filterRest = 'Show All'
    print(filterRest)
    if current_user.is_authenticated:
        restaurants = Restaurant.query.all()

        print("FOOD TAGS")
        print(current_user.fastfood)
        print(current_user.dining)
        print(current_user.dessert)
        print(current_user.chinese)
        print(current_user.pizza)
        print(current_user.healthy)
        print(current_user.bars)
        print(current_user.outside_campus)

        if(filterRest == 'FastFood'):
            current_user.fastfood = current_user.fastfood + 1
        elif(filterRest == 'Dining'):
            current_user.dining = current_user.dining + 1
        elif(filterRest == 'Dessert'):
            current_user.dessert = current_user.dessert + 1
        elif(filterRest == 'Chinese'):
            current_user.chinese = current_user.chinese + 1
        elif(filterRest == 'Pizza'):
            current_user.pizza = current_user.pizza + 1
        elif(filterRest == 'Healthy'):
            current_user.healthy = current_user.healthy + 1
        elif(filterRest == 'Bars'):
            current_user.bars = current_user.bars + 1
        elif(filterRest == 'OutsideCampus'):
            current_user.outside_campus = current_user.outside_campus + 1
        elif(filterRest == 'Show All'):
            current_user.fastfood = current_user.fastfood + 1
            current_user.dining = current_user.dining + 1
            current_user.dessert = current_user.dessert + 1
            current_user.chinese = current_user.chinese + 1
            current_user.pizza = current_user.pizza + 1
            current_user.healthy = current_user.healthy + 1
            current_user.bars = current_user.bars + 1
            current_user.outside_campus = current_user.outside_campus + 1

        
        db.session.commit() #commit the changes made from the statements above
        
        print("FOOD TAGS")
        print(current_user.fastfood)
        print(current_user.dining)
        print(current_user.dessert)
        print(current_user.chinese)
        print(current_user.pizza)
        print(current_user.healthy)
        print(current_user.bars)
        print(current_user.outside_campus)
        
        return render_template('restaurants.html', restaurants=restaurants, base64=base64, form=form, filterRest=filterRest)
    return redirect('login.html')


@main.route('/about_us')
def about_us():
    return render_template("about_us.html")

@main.route('/events')
def list_events():
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day) 
    public_events = Event.query.filter(Event.start_date >= todays_datetime).order_by(Event.start_date).all()
    if not current_user.is_authenticated:
         return redirect('login.html')  

    ev = Event.query.filter_by(host_id = session['user_id']).all()
    hosting_events = []
    if not ev:
            return render_template('events.html', public_events=public_events, base64=base64) 
    for e in ev:
            hosting_events.append(e.id)
    if not hosting_events:
            return render_template('events.html', public_events=public_events, base64=base64) 
    hosted_events = Event.query.filter(Event.id.in_(hosting_events),Event.start_date > todays_datetime).order_by(Event.start_date.desc()).all()
    
    return render_template('events.html', public_events = public_events,  hosted_events = hosted_events,base64=base64)


@main.route('/events/<event_id>')
def display_event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_page.html', event=event, base64=base64)
	
	
@main.route('/create_event', methods=['GET','POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():        
        format = "%Y-%m-%d"
        e = Event(session['user_id'],
                form.title.data,
                form.start_date.data,
                form.end_date.data,
                form.about_me.data,
                form.tags.data,
                form.file.data.read())
        db.session.add(e)
        db.session.commit()
        u = User.query.filter_by(id = session['user_id']).first()
        u.events_attending.append(e)
        db.session.commit()            
        flash('Event is created successfully')
        return redirect(url_for('main.list_events'))
    return render_template('create_event.html', form=form)

@main.route('/cancel_event/<event_id>')
def cancel_event(event_id):
    e = Event.query.filter_by(id = event_id).first()
    if e is None:
        flash('Event does not exist')
        return redirect(url_for('main.list_event'))
    if e.host_id != current_user.id:
        flash('Event can only be cancelled by the host')
        return redirect(url_for('list_events'))
        
    db.session.query(Event).filter(Event.id== event_id).delete()
    db.session.commit()
    flash('Event has been cancelled')
    return redirect(url_for('main.list_events'))

@main.route('/register/<event_id>')
def register_to_event(event_id):
    e = Event.query.filter_by(id = event_id).first()
    if e is None:
        flash('Event does not exist')
        return redirect(url_for('main.list_event'))
    if e.host_id == g.user.id:
        flash('Host cannot register to attend the same event')
        return redirect(url_for('main.list_events'))
    User.query.filter_by(id = session['user_id']).first().events_attending.append(e)
    flash('Registered to attand to this event')
    return redirect(url_for('main.list_events'))   

@main.route('/food/recommendations')
def food_recommendation():
    fastfood = current_user.fastfood
    dining = current_user.dining
    dessert = current_user.dessert
    chinese = current_user.chinese
    bars = current_user.bars
    outside_campus = current_user.outside_campus
    healthy = current_user.healthy
    pizza = current_user.pizza
    
    foodTotal = dining+dessert+chinese+bars+outside_campus+healthy+fastfood+pizza
    print(foodTotal)
    foodProb = {"Dining":dining/foodTotal, "Dessert":dessert/foodTotal, "Pizza":pizza/foodTotal, "Chinese":chinese/foodTotal, "Bars":bars/foodTotal, "OutsideCampus":outside_campus/foodTotal, "Healthy":healthy/foodTotal, "FastFood":fastfood/foodTotal}
    sortedFood = sorted(foodProb.items(), key=operator.itemgetter(1), reverse=True)
    print(sortedFood)
    food = []
    foodWeight = []
    for item in sortedFood:
        food.append(item[0])
        foodWeight.append(item[1])
    print(food)
    print(foodWeight)
    #favoredFood = max(foodProb, key=foodProb.get)
    return(food,foodWeight, sortedFood)
	
@main.route('/activity/recommendations')	
def activity_recommendation():
    nature = current_user.nature
    hiking = current_user.hiking
    extreme = current_user.extreme_sports
    kayaking = current_user.kayaking
    sports = current_user.sports
    concerts = current_user.concerts
    movies = current_user.movies
    ah = current_user.art_history
    st = current_user.science_tech
    ent = current_user.entertainment
    
    actTotal = nature+hiking+extreme+kayaking+sports+concerts+movies+ah+st+ent
    actProb = {"Nature":nature/actTotal, "Concerts":concerts/actTotal, "Hiking":hiking/actTotal, "Extreme":extreme/actTotal, "Kayaking":kayaking/actTotal, "Sports":sports/actTotal, "Movies":movies/actTotal, "Art_History":ah/actTotal, "Science_Tech":st/actTotal, "Entertainment":ent/actTotal}
    sortedActivity = sorted(actProb.items(), key=operator.itemgetter(1), reverse=True)
    print(sortedActivity)
    activity = []
    activityWeight = []
    for item in sortedActivity:
        activity.append(item[0])
        activityWeight.append(item[1])
    print(activity)
    print(activityWeight)
	
	#favoredAct = max(actProb, key=actProb.get)
    return(activity,activityWeight, sortedActivity)
	
	
@main.route('/recommendations')
def recommendations():
    food = food_recommendation()
    activity = activity_recommendation()
    rest = Restaurant.query.all()
    acts = Attraction.query.all() 
                                    ###WRITE TO FILE###
    stats = open("UserProbs.txt", "a")
    stats.write(str(current_user.username)+'\n')
    ##stats.write(str(datetime.now())+'\n')
    stats.write("\nFood Probabilities\n")
    stats.write(str(food[2]))
    stats.write("\nActivities Probabilities\n")
    stats.writelines(str(activity[2])+"\n\n")
    stats.close()

    return render_template('rec.html', food=food, activity=activity, rest=rest, acts=acts, base64=base64)
	
            
    
"""app..jinja_env.filters['formatdatetime'] = format_datetime"""
