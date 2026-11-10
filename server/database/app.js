const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const fs = require('fs');
const Reviews = require('./review');
const Dealerships = require('./dealership');
const app = express();
app.use(express.json({limit:'64kb'}));
app.use(express.urlencoded({extended:false}));
const Counter = mongoose.model('Counter', new mongoose.Schema({_id:String, value:Number}));
const wrap = fn => (req,res,next) => Promise.resolve(fn(req,res,next)).catch(next);
app.get('/', (req,res)=>res.json({service:'Dealerships MongoDB API'}));
app.get('/health', wrap(async(req,res)=>{await mongoose.connection.db.admin().ping();res.json({status:'OK'});}));
app.get('/fetchReviews', wrap(async(req,res)=>res.json(await Reviews.find({},'-_id -__v').sort({id:1}))));
app.get('/fetchReviews/dealer/:id', wrap(async(req,res)=>res.json(await Reviews.find({dealership:Number(req.params.id)},'-_id -__v').sort({id:-1}))));
app.get('/fetchDealers', wrap(async(req,res)=>res.json(await Dealerships.find({},'-_id -__v').sort({id:1}))));
app.get('/fetchDealers/:state', wrap(async(req,res)=>res.json(await Dealerships.find(req.params.state==='All'?{}:{state:req.params.state},'-_id -__v').sort({id:1}))));
app.get('/fetchDealer/:id', wrap(async(req,res)=>res.json(await Dealerships.find({id:Number(req.params.id)},'-_id -__v'))));
app.post('/insert_review', wrap(async(req,res)=>{
 if(process.env.INTERNAL_API_KEY && req.get('X-Internal-Key')!==process.env.INTERNAL_API_KEY)return res.status(403).json({error:'Forbidden'});
 const d=req.body;
 if(!Number.isInteger(Number(d.dealership)) || typeof d.review!=='string' || !d.review.trim() || d.review.length>5000)return res.status(400).json({error:'Invalid review'});
 if(!await Dealerships.exists({id:Number(d.dealership)}))return res.status(404).json({error:'Dealer not found'});
 const seq=await Counter.findOneAndUpdate({_id:'reviews'},{$inc:{value:1}},{new:true});
 const review=new Reviews({id:seq.value,name:d.name,dealership:Number(d.dealership),review:d.review,purchase:d.purchase,purchase_date:d.purchase_date,car_make:d.car_make,car_model:d.car_model,car_year:Number(d.car_year)});
 await review.validate();await review.save();res.status(201).json(review.toObject());
}));
app.use((err,req,res,next)=>res.status(err.name==='ValidationError'?400:500).json({error:err.name==='ValidationError'?'Invalid review data':'Service operation failed'}));
async function start(){
 await mongoose.connect(process.env.MONGODB_URI||'mongodb://127.0.0.1:27018/dealershipsDB');
 await Promise.all([Reviews.init(),Dealerships.init()]);
 for(const [model,file,key] of [[Reviews,'reviews.json','reviews'],[Dealerships,'dealerships.json','dealerships']]){
  const records=JSON.parse(fs.readFileSync(path.join(__dirname,'data',file),'utf8'))[key];
  await model.bulkWrite(records.map(d=>({updateOne:{filter:{id:d.id},update:{$setOnInsert:d},upsert:true}})));
 }
 const max=await Reviews.findOne().sort({id:-1});
 await Counter.updateOne({_id:'reviews'},{$max:{value:max?max.id:0}},{upsert:true});
 const port=process.env.PORT||3030;
 app.listen(port,'0.0.0.0',()=>console.log(`Dealership API listening on ${port}; MongoDB connected and example data seeded.`));
}
if(require.main===module)start().catch(err=>{console.error('Database startup failed:',err.name);process.exit(1);});
module.exports={app,start};
