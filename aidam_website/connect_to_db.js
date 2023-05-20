const express = require('express');
const { ObjectId } = require('mongodb');
const { MongoClient } = require('mongodb');
const app = express();

const uri = 'mongodb+srv://jstrik:strik@cluster0.tk9aheu.mongodb.net/test';
const client = new MongoClient(uri);

app.get('/figure1', async (req, res) => {
  try {
    await client.connect();
    const db = client.db('Main');
    const collections = await db.listCollections().toArray();
    let collectionInfo = [];

    for (const collection of collections) {
      const count = await db.collection(collection.name).countDocuments();
      if (collection.name!='molecules'){
        collectionInfo.push({ name: collection.name, count: count });
      } 
    }

    res.setHeader('Access-Control-Allow-Origin', '*');
    res.send(JSON.stringify(collectionInfo));
  } catch (error) {
    console.error(error);
    res.status(500).send(error.message);
  } finally {
    await client.close();
  }
});

app.get('/figure2and3', async (req, res) => {
  try {
    await client.connect();
    const db = client.db('Main');
    const collections = await db.listCollections().toArray();
    let results = [];

    for (const collection of collections) {
      if (collection.name!='molecules'){
        const result = await db.collection(collection.name).aggregate([
          // { $addFields: { upload_date: { $toDate: "$upload_date" } } },
          { $group: {
              _id: {
                date: "$upload_date",
                uploader: "$uploader"
              },
              count: { $sum: 1 }
            }
          },
          { $sort: { _id: 1 } }
        ]).toArray();
        results.push({ name: collection.name, response: result });
      } 
    }
    console.log(results);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.send(JSON.stringify(results));
  } catch (error) {
    console.error(error);
    res.status(500).send(error.message);
  } finally {
    await client.close();
  }
});

app.get('/search', async (req, res) => {
  try {
    await client.connect();
    const db = client.db('Main');
    const database = req.query.database;
    const namekeyword = req.query.namekeyword;
    const datekeyword = req.query.datekeyword;
    const uploaderkeyword = req.query.uploaderkeyword;
    const collection = db.collection(database);

    const filter = {
      name: { $regex: namekeyword, $options: 'i' },
      upload_date: { $regex: datekeyword },
      uploader: { $regex: uploaderkeyword }
    };

    const result = await collection.find(filter).toArray();
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.send(result);
  } catch (error) {
    console.error(error);
    res.status(500).send(error.message);
  } finally {
    await client.close();
  }
});

// quere specific data from click table line
app.get('/search_one', async (req, res) => {
  try {
    await client.connect();
    const db = client.db('Main');
    const database = req.query.database;
    const collection = db.collection(database);

    const objectId = new ObjectId(req.query._id);

    const result = await collection.findOne({ _id: objectId });
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.send(result);
  } catch (error) {
    console.error(error);
    res.status(500).send(error.message);
  } finally {
    await client.close();
  }
});

app.listen("3000", async () => {
    console.log('Server listening on port 3000, go to http://localhost:3000/');
    try {
        await client.connect();
        collection = client.db("moleculesTestV1").collection("molecules");
    } catch (e) {
        console.error(e);
    }
});