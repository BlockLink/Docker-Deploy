db.b_config.find();
conn = new Mongo();
db = conn.getDB("chaindb");

var cursor = db.b_config.find();
var result = []
while(cursor.hasNext()) {
    r = cursor.next();
    // print(r["_id"] + "\t" + r["key"] + "\t" + r["value"]);
    result.push({
        _id: r['_id'].toString(),
        key: r['key'],
        value: r['value']
    });
}
print(JSON.stringify(result));

