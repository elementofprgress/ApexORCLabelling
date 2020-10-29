from flask import Flask, render_template, request
import sqlite3 as sql
import random

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/apex')
def new_verification():
    # select a random image from the db of unverified images
    con = sql.connect('images_database.db')
    cur = con.cursor()
    sqlite_select_query = """SELECT * from apex_images"""
    cur.execute(sqlite_select_query)
    apex_images_data = cur.fetchall()
    selected_img = random.choice(apex_images_data)

    # create an url using the selected data's filename that matches a stored image's name
    # currently images are stored locally in 'static/images/'
    # TODO: figure out strategy for dealing with some 15k+ images ie. hosted (aws?), locally in static assets, provide images in smaller batches/sets?
    img_url_prefix = ""
    img_url_suffix = ".png"
    img_url = img_url_prefix + str(selected_img[1]) + img_url_suffix

    img_data = {
        "img_name": selected_img[0],
        "img_filename": selected_img[1],
        "orig_pos_x": selected_img[2],
        "orig_pos_y": selected_img[3],
        "orig_pos_z": selected_img[4],
        "pos_x_verified": selected_img[5],
        "pos_y_verified": selected_img[6],
        "pos_z_verified": selected_img[7],
        "img_src": img_url
    }

    return render_template('data_verification.html', data=img_data)


def delete_unverified(con, filename_str):
    sql_delete_query = """DELETE from apex_images where filename = ?"""
    cur = con.cursor()
    cur.execute(sql_delete_query, (filename_str,))
    con.commit()


@app.route('/update', methods=['POST', 'GET'])
def update():
    msg = "tried to get user input data"
    con = sql.connect("images_database.db")
    cur = con.cursor()

    if request.method == 'POST':
        try:
            msg = "tried to update db with user input data"
            print(msg)
            _filename = request.form['_filename']
            _filename_base = request.form['_fname']

            # user input values from form
            _pos_x = request.form['_pos_x']
            _pos_y = request.form['_pos_y']
            _pos_z = request.form['_pos_z']
            print(_filename_base)

            # values from image database either guessed by OCR or previously entered  by user
            _pos_x_verified = request.form['pos_x_verified']
            _pos_y_verified = request.form['pos_y_verified']
            _pos_z_verified = request.form['pos_z_verified']

            # check if user input values match previously entered or guessed values
            if _pos_x == _pos_x_verified and _pos_z == _pos_z_verified and _pos_z == _pos_z_verified:
                print("input values match verify values")

                # create a new filename based on verified input form data.
                new_pos_xyz = _pos_x_verified + " " + _pos_y_verified + " " + _pos_z_verified
                _new_filename = _filename_base + "." + new_pos_xyz

                # original x,y, and z values
                _orig_pos_x = request.form['orig_pos_x']
                _orig_pos_y = request.form['orig_pos_y']
                _orig_pos_z = request.form['orig_pos_z']

                # add verified data to verified images data base
                # include the orig and new filename along with the orig and new x,y,z values
                try:
                    cur.execute('INSERT INTO verified_apex_images VALUES(?,?,?,?,?,?,?,?);', (_filename, _new_filename, _orig_pos_x, _orig_pos_y, _orig_pos_z, _pos_x, _pos_y, _pos_z))
                except sql.Error as e:
                    print("ERROR: "+e)
                con.commit()

                # TODO: verify successful write to db before deleting unverified database entry
                print("image added to verified, delete from unverified")
                delete_unverified(con, _filename)
            else:
                cur.execute('UPDATE apex_images SET verify_pos_x=?, verify_pos_y=?, verify_pos_z=? WHERE filename_base=?', [_pos_x, _pos_y, _pos_z, _filename_base])
            con.commit()
            con.close()
            msg = _filename + ": user values added to db to verify"
        except sql.Error as error:
            msg = "ERROR: " + _filename + " - user input values not added to databases due to: " + error
            print("error while updating databases with user input data", error)

        finally:
            if con:
                con.close()
            return render_template("result.html", msg=msg)


@app.route('/db')
def db():
    con = sql.connect("images_database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from apex_images")
    rows = cur.fetchall()

    cur0 = con.cursor()
    cur0.execute("select * from verified_apex_images")
    verified_rows = cur0.fetchall()

    return render_template("list.html", rows=rows, verified_rows=verified_rows)


if __name__ == '__main__':
    app.run()
