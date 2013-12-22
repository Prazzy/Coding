function MakeList(size) {
   head = {'data':'', 'next':null};
   prev = head;
   for (var i=0;i<size;i++){
       var curr_obj = {};
       curr_obj.data = i+1;
       prev.next = curr_obj;
       prev = curr_obj;
   }
   return head;
}


function PrintNodes(head) {
  var node = head.next;
  while (node) {
    console.log(node.data);
    node = node.next;  
  }
}

console.log(PrintNodes(MakeList(3)));

function ReverseList(head) {
   var node = head.next;
    head.next = {};
   var prev = null;
   while (node) {
       if (node.next) {saved = node.next;}
       else {head.next = node; saved=null;}
     node.next = prev;
     prev = node;
     node = saved;
   }
  return head;
}

console.log(PrintNodes(ReverseList(MakeList(3))));




