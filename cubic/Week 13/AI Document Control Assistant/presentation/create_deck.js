const pptxgen = require('pptxgenjs');
const path = require('path');
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Cubic Engineering Consultancy';
pptx.subject = 'Week 13 AI Document Control Assistant Platform';
pptx.title = 'AI Document Control Assistant Demo Presentation';
pptx.company = 'Cubic Engineering Consultancy';
pptx.lang = 'en-US';
pptx.theme = {
  headFontFace: 'Aptos Display', bodyFontFace: 'Aptos', lang: 'en-US'
};
pptx.defineLayout({ name: 'CUSTOM_WIDE', width: 13.333, height: 7.5 });
pptx.layout = 'CUSTOM_WIDE';
const W = 13.333, H = 7.5;
const COLORS = { navy:'172033', blue:'2457D6', pale:'EEF3FF', gray:'53657D', light:'F7F9FC', green:'2E7D32', amber:'B26A00', red:'B42318', white:'FFFFFF' };
function addBg(slide){ slide.background = { color: COLORS.white }; slide.addShape(pptx.ShapeType.rect,{x:0,y:0,w:W,h:H,fill:{color:'FFFFFF'},line:{color:'FFFFFF'}}); }
function title(slide,t,sub){ slide.addText(t,{x:0.55,y:0.35,w:8.8,h:0.45,fontFace:'Aptos Display',fontSize:27,bold:true,color:COLORS.navy,margin:0}); if(sub) slide.addText(sub,{x:0.58,y:0.86,w:7.8,h:0.28,fontSize:11,color:COLORS.gray,margin:0}); }
function footer(slide,n){ slide.addText('Cubic Engineering Consultancy | Week 13 Final Demonstration',{x:0.55,y:7.05,w:6.8,h:0.2,fontSize:8,color:'7A8496',margin:0}); slide.addText(String(n),{x:12.45,y:7.05,w:0.3,h:0.2,fontSize:8,color:'7A8496',margin:0,align:'right'}); }
function box(slide,text,x,y,w,h,opts={}){ slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h,rectRadius:0.08,fill:{color:opts.fill||COLORS.pale},line:{color:opts.line||'D8E1F7',width:1}}); slide.addText(text,{x:x+0.12,y:y+0.10,w:w-0.24,h:h-0.16,fontSize:opts.fs||14,bold:opts.bold||false,color:opts.color||COLORS.navy,breakLine:false,fit:'shrink',margin:0.02,align:opts.align||'center',valign:'mid'}); return {x,y,w,h}; }
function pill(slide,text,x,y,w,color){ slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h:0.35,rectRadius:0.12,fill:{color},line:{color}}); slide.addText(text,{x:x+0.08,y:y+0.08,w:w-0.16,h:0.15,fontSize:10,bold:true,color:COLORS.white,align:'center',margin:0}); return {x,y,w,h:0.35}; }
function warnIfSlideElementsOutOfBounds(slideName, elems){ const bad = elems.filter(e=>e.x<0||e.y<0||e.x+e.w>W||e.y+e.h>H); if(bad.length) console.warn(`Out of bounds on ${slideName}: ${bad.length}`); }
function overlap(a,b){ return Math.max(0, Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)) * Math.max(0, Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)); }
function warnIfSlideHasOverlaps(slideName, elems){ let count=0; for(let i=0;i<elems.length;i++){ for(let j=i+1;j<elems.length;j++){ const area=overlap(elems[i],elems[j]); const minArea=Math.min(elems[i].w*elems[i].h, elems[j].w*elems[j].h); if(area>0.08*minArea) count++; }} if(count) console.warn(`Possible overlaps on ${slideName}: ${count}`); }
function validate(name, elems){ warnIfSlideElementsOutOfBounds(name, elems); warnIfSlideHasOverlaps(name, elems); }

let s, elems=[];
// 1
s=pptx.addSlide(); addBg(s); elems=[];
s.addText('AI Document Control Assistant',{x:0.7,y:1.1,w:7.8,h:0.7,fontFace:'Aptos Display',fontSize:40,bold:true,color:COLORS.navy,margin:0});
s.addText('Unified platform for document intake, AI metadata, workflow control, audit trail, analytics, and final reporting.',{x:0.75,y:2.05,w:6.8,h:0.75,fontSize:19,color:COLORS.gray,breakLine:false,fit:'shrink',margin:0});
elems.push({x:0.7,y:1.1,w:7.8,h:1.8});
elems.push(pill(s,'Week 13 Final Demonstration',0.75,3.05,2.85,COLORS.blue));
s.addImage({path:path.join(__dirname,'../docs/architecture_diagram.png'),x:8.75,y:1.35,w:3.95,h:2.8}); elems.push({x:8.75,y:1.35,w:3.95,h:2.8});
box(s,'End-to-end lifecycle: Draft -> Review -> Approve -> Issue -> Archive',1.0,5.0,11.3,0.7,{fill:'F7F9FC',fs:19,bold:true}); elems.push({x:1,y:5,w:11.3,h:.7}); footer(s,1); validate('slide 1',elems);
//2
s=pptx.addSlide(); addBg(s); title(s,'What was integrated','A single platform combines all previously developed document-control modules.'); elems=[];
const mods=[['Intake','source text and sample records'],['AI engine','metadata, discipline, type, confidence, risk'],['Workflow','controlled states and transition validation'],['Audit','traceable event history'],['Analytics','status, discipline, risk, and performance KPIs']];
mods.forEach((m,i)=>{elems.push(box(s,`${m[0]}\n${m[1]}`,0.65+i*2.5,2.0,2.15,1.45,{fs:14,bold:true,fill:i%2?'F7F9FC':'EEF3FF'})); if(i<mods.length-1){s.addShape(pptx.ShapeType.rightArrow,{x:2.72+i*2.5,y:2.45,w:0.42,h:0.28,fill:{color:'B8C6EA'},line:{color:'B8C6EA'}});}});
box(s,'Result: one deployable FastAPI dashboard with API endpoints, database, tests, reports, documentation, and presentation.',1.05,4.55,11.2,0.95,{fill:'FFFFFF',line:'D8E1F7',fs:20,bold:true}); elems.push({x:1.05,y:4.55,w:11.2,h:.95}); footer(s,2); validate('slide 2',elems);
//3
s=pptx.addSlide(); addBg(s); title(s,'Platform architecture','Service boundaries keep the final demo complete and future-ready.'); elems=[];
s.addImage({path:path.join(__dirname,'../docs/architecture_diagram.png'),x:0.75,y:1.55,w:11.85,h:4.7}); elems.push({x:.75,y:1.55,w:11.85,h:4.7});
footer(s,3); validate('slide 3',elems);
//4
s=pptx.addSlide(); addBg(s); title(s,'Controlled workflow states','Documents move through a traceable lifecycle with validation rules.'); elems=[];
const wf=[['Draft','Created and classified'],['In Review','Engineering review'],['Approved','Ready to issue'],['Issued','Released to team'],['Archived','Controlled record']];
wf.forEach((m,i)=>{elems.push(box(s,`${m[0]}\n${m[1]}`,0.7+i*2.55,2.0,2.05,1.0,{fs:13,bold:true,fill:i==0?'EEF3FF':i==1?'FFF7E8':i==2?'EAF7ED':i==3?'EAF0FF':'F7F9FC'})); if(i<wf.length-1){s.addShape(pptx.ShapeType.rightArrow,{x:2.66+i*2.55,y:2.34,w:0.45,h:0.3,fill:{color:'A9B8DC'},line:{color:'A9B8DC'}});}});
box(s,'Rejected documents return to Draft for correction, creating a visible audit trail instead of uncontrolled revision changes.',1.2,4.55,10.9,0.85,{fs:18,bold:true,fill:'FFFFFF'}); elems.push({x:1.2,y:4.55,w:10.9,h:.85}); footer(s,4); validate('slide 4',elems);
//5
s=pptx.addSlide(); addBg(s); title(s,'Dashboard and reporting','The web interface turns the document register into operational KPIs.'); elems=[];
s.addChart(pptx.ChartType.bar,[{name:'Documents',labels:['Draft','In Review','Approved','Issued','Archived'],values:[1,2,1,1,0]}], {x:0.8,y:1.65,w:5.4,h:3.6,catAxisLabelFontFace:'Aptos',catAxisLabelFontSize:10,valAxisLabelFontSize:10,showLegend:false,showTitle:false,showValue:false,valAxisMinVal:0,valAxisMaxVal:3}); elems.push({x:.8,y:1.65,w:5.4,h:3.6});
box(s,'Core KPIs\nTotal documents\nOpen reviews\nAverage confidence\nHigh-risk count',7.2,1.8,4.9,1.7,{fill:'F7F9FC',fs:18,bold:true}); elems.push({x:7.2,y:1.8,w:4.9,h:1.7});
box(s,'Reporting outputs are available in the dashboard and through `/api/analytics/summary` for integration.',7.2,4.15,4.9,0.85,{fill:'FFFFFF',fs:15,bold:false}); elems.push({x:7.2,y:4.15,w:4.9,h:.85}); footer(s,5); validate('slide 5',elems);
//6
s=pptx.addSlide(); addBg(s); title(s,'AI metadata and classification','The demo uses explainable, testable logic for safe final demonstration.'); elems=[];
elems.push(box(s,'Extracted metadata\nTitle\nDocument number\nRevision',0.85,1.75,3.55,1.6,{fs:18,bold:true,fill:'EEF3FF'}));
elems.push(box(s,'Classification\nDiscipline\nDocument type\nConfidence score',4.9,1.75,3.55,1.6,{fs:18,bold:true,fill:'F7F9FC'}));
elems.push(box(s,'Risk scoring\nKeywords\nReview urgency\nAudit support',8.95,1.75,3.55,1.6,{fs:18,bold:true,fill:'FFF7E8'}));
box(s,'Accuracy report: 5 demo test cases, 100% discipline accuracy, 100% document-type accuracy, 0.19 ms average latency per document.',1.05,4.75,11.2,0.8,{fs:19,bold:true,fill:'FFFFFF'}); elems.push({x:1.05,y:4.75,w:11.2,h:.8}); footer(s,6); validate('slide 6',elems);
//7
s=pptx.addSlide(); addBg(s); title(s,'End-to-end demonstration path','The demo proves the complete lifecycle rather than isolated scripts.'); elems=[];
const steps=['Seed sample records','Open dashboard','Review document detail','Apply workflow transition','Inspect audit trail','Run tests and evaluation'];
steps.forEach((st,i)=>{const x=i<3?0.9+i*4.1:0.9+(i-3)*4.1; const y=i<3?1.65:4.15; elems.push(box(s,`${i+1}. ${st}`,x,y,3.5,0.95,{fs:18,bold:true,fill:i%2?'F7F9FC':'EEF3FF'}));});
footer(s,7); validate('slide 7',elems);
//8
s=pptx.addSlide(); addBg(s); title(s,'Final deliverables','Week 13 package is ready for submission and demonstration.'); elems=[];
const deliv=['Integrated FastAPI platform','Dashboard and workflow states','Architecture diagram','Technical documentation','Accuracy and performance report','Demo presentation'];
deliv.forEach((d,i)=>{const x=i%2?6.9:1.0; const y=1.5+Math.floor(i/2)*1.25; elems.push(box(s,d,x,y,5.1,0.72,{fs:18,bold:true,fill:'F7F9FC'}));});
box(s,'Submission-ready project folder: cubic/Week 13/AI Document Control Assistant',1.0,5.75,11.0,0.62,{fs:18,bold:true,fill:'EEF3FF'}); elems.push({x:1,y:5.75,w:11,h:.62}); footer(s,8); validate('slide 8',elems);

pptx.writeFile({ fileName: path.join(__dirname,'AI_Document_Control_Assistant_Demo_Presentation.pptx') });
