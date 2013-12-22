

function MakeNode(size) {
   head = {'data':'', 'next':null};
   prev = head;
   for (var i=0;i<size;i++){
       var curr_obj = {};
       curr_obj['data'] = i+1;
       prev.next = curr_obj;
       prev = curr_obj;
   }
   return head;
}


