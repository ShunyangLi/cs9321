from flask import Flask, jsonify, make_response, request
import pandas as pd
from flask_restplus import Api, Resource, abort, fields

app = Flask(__name__)
api = Api(app)


args = api.model('Book', {
    'Flickr_URL': fields.String,
    'Publisher': fields.String,
    'Author': fields.String,
    'Title': fields.String,
    'Date_of_Publication': fields.Integer,
    'Identifier': fields.Integer,
    'Place_of_Publication': fields.String
})


@api.route('/books/<int:id>')
class Books(Resource):

    def get(self, id):
        if id not in df.index:
            abort(404, "Can not find: %s"%id)

        data = df.loc[id].to_json()
        return make_response(jsonify(data=data))

    def delete(self, id):
        if id not in df.index:
            abort(404, "Can not find: %s" % id)

        df.drop(id)
        return make_response(jsonify(message='Success'), 200)

    @api.expect(args)
    def put(self, id):
        if id not in df.index:
            abort(404, "Can not find: %s" % id)

        book = request.json

        print(book)

        if 'Identifier' in book and id != book['Identifier']:
            return {"message": "Identifier cannot be changed".format(id)}, 400

        # Update the values
        for key in book:
            if key not in args.keys():
                # unexpected column
                return {"message": "Property {} is invalid".format(key)}, 400
            df.loc[id, key] = book[key]

        # df.append(book, ignore_index=True)
        return {"message": "Book {} has been successfully updated".format(id)}, 200


if __name__ == '__main__':
    df = pd.read_csv('Books.csv')
    col = [
        'Edition Statement',
        'Corporate Author',
        'Corporate Contributors',
        'Former owner',
        'Engraver',
        'Contributors',
        'Issuance type',
        'Shelfmarks'
    ]

    df.drop(columns=col, inplace=True, axis=1)
    df.set_index('Identifier')

    new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    new_date = pd.to_numeric(new_date)
    new_date = new_date.fillna(0)
    df['Date of Publication'] = new_date
    df.columns = [str(x).replace(' ', '_') for x in df.columns]
    app.run(debug=True)
