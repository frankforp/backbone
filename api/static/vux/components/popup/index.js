/*!
 * Vux v0.1.3 (https://vux.li)
 * Licensed under the MIT license
 */
!function(t,n){"object"==typeof exports&&"object"==typeof module?module.exports=n():"function"==typeof define&&define.amd?define([],n):"object"==typeof exports?exports.vuxPopup=n():t.vuxPopup=n()}(this,function(){return function(t){function n(e){if(o[e])return o[e].exports;var r=o[e]={exports:{},id:e,loaded:!1};return t[e].call(r.exports,r,r.exports,n),r.loaded=!0,r.exports}var o={};return n.m=t,n.c=o,n.p="",n(0)}([function(t,n,o){t.exports=o(40)},function(t,n){var o=t.exports={version:"2.4.0"};"number"==typeof __e&&(__e=o)},function(t,n,o){t.exports=!o(3)(function(){return 7!=Object.defineProperty({},"a",{get:function(){return 7}}).a})},function(t,n){t.exports=function(t){try{return!!t()}catch(n){return!0}}},function(t,n){var o=t.exports="undefined"!=typeof window&&window.Math==Math?window:"undefined"!=typeof self&&self.Math==Math?self:Function("return this")();"number"==typeof __g&&(__g=o)},function(t,n){t.exports=function(t){return"object"==typeof t?null!==t:"function"==typeof t}},function(t,n){t.exports=function(t){if(void 0==t)throw TypeError("Can't call method on  "+t);return t}},function(t,n){var o=Math.ceil,e=Math.floor;t.exports=function(t){return isNaN(t=+t)?0:(t>0?e:o)(t)}},function(t,n,o){var e=o(24),r=o(6);t.exports=function(t){return e(r(t))}},function(t,n,o){"use strict";function e(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(n,"__esModule",{value:!0});var r=o(11),i=e(r),u=o(10),s=e(u);n["default"]={props:{show:{type:Boolean,twoWay:!0},height:{type:String,"default":"auto"},hideOnBlur:{type:Boolean,"default":!0}},ready:function(){var t=this;this.popup=new s["default"]({container:t.$el,innerHTML:"",hideOnBlur:t.hideOnBlur,onOpen:function(n){t.fixSafariOverflowScrolling("auto"),t.show=!0},onClose:function(n){t.show=!1,(0,i["default"])(window.__$vuxPopups).length>=1||t.fixSafariOverflowScrolling("touch")}}),this.$overflowScrollingList=document.querySelectorAll(".vux-fix-safari-overflow-scrolling")},methods:{fixSafariOverflowScrolling:function(t){if(this.$overflowScrollingList.length&&/iphone/i.test(navigator.userAgent))for(var n=0;n<this.$overflowScrollingList.length;n++)this.$overflowScrollingList[n].style.webkitOverflowScrolling=t}},data:function(){return{hasFirstShow:!1}},watch:{show:function(t){t?(this.popup.show(),this.$emit("on-show"),this.hasFirstShow||(this.$emit("on-first-show"),this.hasFirstShow=!0)):(this.$emit("on-hide"),this.show=!1,this.popup.hide(!1))}},beforeDestroy:function(){this.popup.destroy(),this.fixSafariOverflowScrolling("touch")}}},function(t,n){"use strict";Object.defineProperty(n,"__esModule",{value:!0}),window.__$vuxPopups=window.__$vuxPopups||{};var o=function(t){this.uuid=Math.random().toString(36).substring(3,8),this.params={},this.isShow=!1,"[object Object]"===Object.prototype.toString.call(t)&&(this.params={input:t.input||"",container:document.querySelector(t.input)||"",innerHTML:t.innerHTML||"",hideOnBlur:t.hideOnBlur,onOpen:t.onOpen||function(){},onClose:t.onClose||function(){}}),!!document.querySelectorAll(".vux-popup-mask").length<=0&&(this.divMask=document.createElement("a"),this.divMask.className="vux-popup-mask",this.divMask.href="javascript:void(0)",document.body.appendChild(this.divMask));var n=void 0;return n=t.container?t.container:document.createElement("div"),n.className="vux-popup-dialog vux-popup-dialog-"+this.uuid,t.container||document.body.appendChild(n),this.mask=document.querySelector(".vux-popup-mask"),this.container=document.querySelector(".vux-popup-dialog-"+this.uuid),this._bindEvents(),t=null,this};o.prototype.onClickMask=function(){this.params.hideOnBlur&&this.isShow&&this.hide(!1)},o.prototype._bindEvents=function(){this.params.hideOnBlur&&this.mask.addEventListener("click",this.onClickMask.bind(this),!1)},o.prototype.show=function(){this.mask.classList.add("vux-popup-show"),this.container.classList.add("vux-popup-show"),this.params.onOpen&&this.params.onOpen(this),this.isShow=!0,window.__$vuxPopups[this.uuid]=1},o.prototype.hide=function(){var t=arguments.length<=0||void 0===arguments[0]?!0:arguments[0];this.container.classList.remove("vux-popup-show"),document.querySelector(".vux-popup-dialog.vux-popup-show")||this.mask.classList.remove("vux-popup-show"),t===!1&&this.params.onClose&&this.params.hideOnBlur&&this.params.onClose(this),this.isShow=!1,delete window.__$vuxPopups[this.uuid]},o.prototype.html=function(t){this.container.innerHTML=t},o.prototype.destroy=function(){this.mask.removeEventListener("click",this.onClickMask.bind(this),!1),this.mask&&this.mask.parentNode&&this.mask.parentNode.removeChild(this.mask),delete window.__$vuxPopups[this.uuid]},n["default"]=o},function(t,n,o){t.exports={"default":o(12),__esModule:!0}},function(t,n,o){o(37),t.exports=o(1).Object.keys},function(t,n){t.exports=function(t){if("function"!=typeof t)throw TypeError(t+" is not a function!");return t}},function(t,n,o){var e=o(5);t.exports=function(t){if(!e(t))throw TypeError(t+" is not an object!");return t}},function(t,n,o){var e=o(8),r=o(33),i=o(32);t.exports=function(t){return function(n,o,u){var s,c=e(n),p=r(c.length),a=i(u,p);if(t&&o!=o){for(;p>a;)if(s=c[a++],s!=s)return!0}else for(;p>a;a++)if((t||a in c)&&c[a]===o)return t||a||0;return!t&&-1}}},function(t,n){var o={}.toString;t.exports=function(t){return o.call(t).slice(8,-1)}},function(t,n,o){var e=o(13);t.exports=function(t,n,o){if(e(t),void 0===n)return t;switch(o){case 1:return function(o){return t.call(n,o)};case 2:return function(o,e){return t.call(n,o,e)};case 3:return function(o,e,r){return t.call(n,o,e,r)}}return function(){return t.apply(n,arguments)}}},function(t,n,o){var e=o(5),r=o(4).document,i=e(r)&&e(r.createElement);t.exports=function(t){return i?r.createElement(t):{}}},function(t,n){t.exports="constructor,hasOwnProperty,isPrototypeOf,propertyIsEnumerable,toLocaleString,toString,valueOf".split(",")},function(t,n,o){var e=o(4),r=o(1),i=o(17),u=o(22),s="prototype",c=function(t,n,o){var p,a,f,l=t&c.F,h=t&c.G,d=t&c.S,v=t&c.P,x=t&c.B,w=t&c.W,y=h?r:r[n]||(r[n]={}),m=y[s],g=h?e:d?e[n]:(e[n]||{})[s];h&&(o=n);for(p in o)a=!l&&g&&void 0!==g[p],a&&p in y||(f=a?g[p]:o[p],y[p]=h&&"function"!=typeof g[p]?o[p]:x&&a?i(f,e):w&&g[p]==f?function(t){var n=function(n,o,e){if(this instanceof t){switch(arguments.length){case 0:return new t;case 1:return new t(n);case 2:return new t(n,o)}return new t(n,o,e)}return t.apply(this,arguments)};return n[s]=t[s],n}(f):v&&"function"==typeof f?i(Function.call,f):f,v&&((y.virtual||(y.virtual={}))[p]=f,t&c.R&&m&&!m[p]&&u(m,p,f)))};c.F=1,c.G=2,c.S=4,c.P=8,c.B=16,c.W=32,c.U=64,c.R=128,t.exports=c},function(t,n){var o={}.hasOwnProperty;t.exports=function(t,n){return o.call(t,n)}},function(t,n,o){var e=o(25),r=o(29);t.exports=o(2)?function(t,n,o){return e.f(t,n,r(1,o))}:function(t,n,o){return t[n]=o,t}},function(t,n,o){t.exports=!o(2)&&!o(3)(function(){return 7!=Object.defineProperty(o(18)("div"),"a",{get:function(){return 7}}).a})},function(t,n,o){var e=o(16);t.exports=Object("z").propertyIsEnumerable(0)?Object:function(t){return"String"==e(t)?t.split(""):Object(t)}},function(t,n,o){var e=o(14),r=o(23),i=o(35),u=Object.defineProperty;n.f=o(2)?Object.defineProperty:function(t,n,o){if(e(t),n=i(n,!0),e(o),r)try{return u(t,n,o)}catch(s){}if("get"in o||"set"in o)throw TypeError("Accessors not supported!");return"value"in o&&(t[n]=o.value),t}},function(t,n,o){var e=o(21),r=o(8),i=o(15)(!1),u=o(30)("IE_PROTO");t.exports=function(t,n){var o,s=r(t),c=0,p=[];for(o in s)o!=u&&e(s,o)&&p.push(o);for(;n.length>c;)e(s,o=n[c++])&&(~i(p,o)||p.push(o));return p}},function(t,n,o){var e=o(26),r=o(19);t.exports=Object.keys||function(t){return e(t,r)}},function(t,n,o){var e=o(20),r=o(1),i=o(3);t.exports=function(t,n){var o=(r.Object||{})[t]||Object[t],u={};u[t]=n(o),e(e.S+e.F*i(function(){o(1)}),"Object",u)}},function(t,n){t.exports=function(t,n){return{enumerable:!(1&t),configurable:!(2&t),writable:!(4&t),value:n}}},function(t,n,o){var e=o(31)("keys"),r=o(36);t.exports=function(t){return e[t]||(e[t]=r(t))}},function(t,n,o){var e=o(4),r="__core-js_shared__",i=e[r]||(e[r]={});t.exports=function(t){return i[t]||(i[t]={})}},function(t,n,o){var e=o(7),r=Math.max,i=Math.min;t.exports=function(t,n){return t=e(t),0>t?r(t+n,0):i(t,n)}},function(t,n,o){var e=o(7),r=Math.min;t.exports=function(t){return t>0?r(e(t),9007199254740991):0}},function(t,n,o){var e=o(6);t.exports=function(t){return Object(e(t))}},function(t,n,o){var e=o(5);t.exports=function(t,n){if(!e(t))return t;var o,r;if(n&&"function"==typeof(o=t.toString)&&!e(r=o.call(t)))return r;if("function"==typeof(o=t.valueOf)&&!e(r=o.call(t)))return r;if(!n&&"function"==typeof(o=t.toString)&&!e(r=o.call(t)))return r;throw TypeError("Can't convert object to primitive value")}},function(t,n){var o=0,e=Math.random();t.exports=function(t){return"Symbol(".concat(void 0===t?"":t,")_",(++o+e).toString(36))}},function(t,n,o){var e=o(34),r=o(27);o(28)("keys",function(){return function(t){return r(e(t))}})},function(t,n){},function(t,n){t.exports="<div v-show=show transition=vux-popup :style={height:height} class=vux-popup> <slot></slot> </div>"},function(t,n,o){var e,r;o(38),e=o(9),r=o(39),t.exports=e||{},t.exports.__esModule&&(t.exports=t.exports["default"]),r&&(("function"==typeof t.exports?t.exports.options||(t.exports.options={}):t.exports).template=r)}])});