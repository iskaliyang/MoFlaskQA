from flask import Blueprint, render_template, request, session, redirect, url_for, g

from application import db
from libs.decoration import logon_required
from libs.models import Question, User, Comment

qa = Blueprint('qa', __name__)


@qa.route('/list')
def lists():
    """
    问答列表
    :return:
    """
    return render_template('home/qa/qa_list.html')


@qa.route('/release/', methods=['GET', 'POST'])
@logon_required
def release_qa():
    """
    问答发布视图
    :return:
    """
    if request.method == 'GET':
        return render_template('home/qa/release_qa.html')
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        q = Question(title=title, content=content)
        q.author = User.query.filter_by(id=session.get('user_id')).first()
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('home.index'))


@qa.route('/detail/<int:question_id>')
def detail(question_id):
    question = Question.query.filter_by(id=question_id).first()
    comments = question.comments
    context = {
        'question': question,
        'total_comments': len(comments)
    }
    return render_template('home/qa/detail.html', **context)


@qa.route('/comment', methods=['POST'])
@logon_required
def comment():
    """
    评论
    :return:
    """
    content = request.form.get('content')  # content：是内容，comment是评论
    question_id = request.form.get('question_id')
    user_id = session.get('user_id')

    if content is None:
        return redirect(url_for('qa.detail', question_id=question_id))

    question = Question.query.filter_by(id=question_id).first()
    user = User.query.filter_by(id=user_id).first()

    com = Comment(content=content)
    com.question = question
    com.author = user
    db.session.add(com)
    db.session.commit()
    # 跳转本蓝图内不加蓝图名
    return redirect(url_for('qa.detail', question_id=question_id))
