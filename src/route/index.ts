import * as express from 'express';
import {register} from './register';
import {infoRouter} from './info';
const router = express.Router();

router.get('/',(req:any,res,next)=>{
    if(req.session.userinfo) {
        res.redirect("/info");
    }else{
        res.redirect("/static/register.html");
    }
});

router.use('/register',register);
router.use('/info',infoRouter);

export {
    router
}
