'''
Created on Jan 4, 2013

@author: Praveen
'''
import Queue
import time
import math
import collections

from multiprocessing.managers import SyncManager 

# Constants

IP_ADDRESS = ''
PORT_NUM = 50000
WORKERS_COUNT = 3
TEXT1 = """On the sultry third of July, 1778, Fred Godfrey, a sturdy youth of eighteen years, was riding at a breakneck speed down the Wyoming Valley, in the direction of the settlement, from which he saw columns of smoke rolling upward, and whence, during the few pauses of his steed, he heard the rattling discharge of firearms and the shouts of combatants.

"I wonder whether I am too late," he asked himself more than once, and he urged his splendid horse to a greater pace; "the road never seemed so long."

Ah, there was good cause for the anxiety of the lad, for in that lovely Wyoming Valley lived those who were dearer to him than all the world beside, and whatever fate overtook the settlers must be shared by him as well. He had ridden his horse hard, and his flanks glistened with wet and foam, but though every foot of the winding road was familiar to him, it appeared in his torturing impatience to be double its usual length.

Fred Godfrey had received the promise of his father, on the breaking out of the Revolution, that he might enlist in the patriot army so soon as he reached the age of seventeen. On the very day that he attained that age he donned the Continental uniform, made for him by loving hands, bade his friends good-bye, and hastened away to where Washington was longing for just such lusty youths as he who appeared to be several years younger than he really was."""

TEXT2 = """Fred was a handsome, athletic youngster, and he sat his horse with the grace of a crusader. Although the day was warm, and his face glowed with perspiration, he wore his cocked hat, blue coat with its white facings, the belt around the waist and another which passed over one shoulder ere it joined the one around the middle of his body, knee-breeches, and strong stockings and shoes. His rifle was slung across his back, and a couple of loaded single-barreled pistols were thrust in his belt, where they could be drawn the instant needed.

During his year's service in the patriot army Fred had proven himself an excellent soldier, and the dash and nerve which he showed in more than one instance caught the eye of Washington himself, and won the youth a lieutenancy, at the time when he was the youngest member of his company.

The ardent patriot was full of ambition, and was sure, should no accident befall him, of gaining higher honors. When he tramped with several other recruits from Wyoming to the camp of the Continentals, hundreds of miles away, one of his greatest comforts was the belief that, no matter how the current of war drifted back and forth, there was no danger of its reaching Wyoming. That lovely and secluded valley was so far removed from the tread of the fierce hosts that they might feel secure.

But behold! News came to Washington that the Tories and Indians were about to march into the valley with torch and tomahawk, and he was begged to send re-enforcements without delay. The Father of his Country was then on his campaign through the Jerseys. The British army had withdrawn from Philadelphia, where it spent the winter, and Clinton with a part of the force was marching overland to New York, with the Continentals in pursuit."""

TEXT3 = """The campaign was so important that the commander-in-chief could ill afford to spare a man. He knew that Wyoming was not entirely defenseless. Colonel Zebulon Butler of the Continental army was marshaling the old men and boys, and there was the strong defense known as Forty Fort, built by the original settlers from Connecticut, not to mention Wilkesbarre near at hand, so that it would seem the settlers ought to be able to protect themselves against any force likely to be brought against them.

However, Washington told several of his recruits from Wyoming of the appeal that had been made to him, and gave them permission to go to the help of their friends, though he added that he did not think it possible for them to reach the ground in time to be of service.

But a half dozen started on foot toward the threatened point. Within a day's tramp of their destination they fell somewhat apart, as each, in his familiarity of the country, believed that he knew a shorter and quicker way home than the others.

Fred Godfrey was almost in sight of his home, when he was both pleased and alarmed by coming upon an estray horse. He was saddled and bridled, and though contentedly cropping the grass at the roadside, the perspiration and jaded look showed that he had come from the battle-ground. It was startling to know that such was the fact, and supplemented as it was by the reports of guns, shouts, and the black volumes of smoke pouring upward, Fred was filled with an anguish of misgiving.

Without stopping to make inquiries or to guess who could have owned the estray steed, the young patriot slipped forward, caught the bridle before the animal had time to scent danger, and vaulting lightly into the saddle, turned the head of the horse toward Wyoming, and striking his heels against his ribs, quickly urged him to a dead run.

"I am needed there," said Fred, urging his spirited animal still more, and peering down the highway; "you're the best horse I ever rode, but I can't afford to spare you now."

Fred Godfrey not only was close to the stirring scenes that marked that memorable massacre, but he was among them sooner even than he anticipated."""

TEXT4 = """Just here we must turn aside for a minute or two, in order to understand the situation.

On the third of July, Colonel Zebulon Butler, of the Continental army, had marched forth at the head of his two hundred and odd boys, old men, and a few able-bodied soldiers to meet his cousin, the British Colonel Butler, with his horde of soldiers, Tories, and Iroquois Indians.

For a time all went well, and Colonel Zebulon Butler began to hope that the marauders would be driven off, but his force was unsteady, and some of them gave way when they saw their enemies as they swarmed out of the woods and assailed them.

Some might succeed in reaching the mountains on the other side the river, and possibly a few would be able to force their way through the dismal wilderness known as the "Shades of Death," and reach Stroudsburg and the sparse settlements on the upper Delaware, many miles away.

The moment the patriots began flying before the Tories and Indians, the panic spread to all.

It is a historical fact that in the flight the pursuers shot many of the patriot officers and soldiers in the thigh, so as to disable them from running, and left them on the ground to be finally disposed of afterwards, while the Iroquois hastened after the other fugitives.

Many of these were tomahawked in their flight; others fled down the river banks in the direction of Wilkesbarre, on the opposite side of the river; others made for the mountains back of the battle-ground; still others hastened to the protection of the Forty Fort, while a great many found a temporary refuge in the undergrowth of Monocacy Island, in the Susquehanna. Still others got across the river and plunged into the mountainous wilderness and began their toilsome tramp through the section I have named, and which is still known as the "Shades of Death."

It was at this hour that Fred Godfrey galloped directly into the massacre in his desperate resolve to do all he could to save his friends.

Some one fired from the front, and undoubtedly would have struck the youthful rider, had not his horse at the very instant snuffed the danger and flung up his head. The action saved the life of the rider at the expense of the steed, who received the cruel bullet and lunged forward and fell to the ground with such suddenness that but for the dexterity of Fred Godfrey he would have been crushed.

As it was, the youth saved himself by a hair's breadth, leaping clear of the saddle and brute just in the nick of time.

The thin wreath of smoke was curling upward from the undergrowth, and the horse was in the act of falling, when a Seneca Indian, in his war paint and agleam with ferocity, bounded from the cover, and with his smoking gun in his hand and the other grasping the handle of his tomahawk, dashed towards the patriot, whom he evidently believed was badly wounded.

"S'render! s'render!" he shrieked, coming down upon him as if fired from a cannon.

"I'm not in that business just now," snapped out Fred Godfrey, leveling and firing his pistol, with the muzzle almost in the face of the fierce warrior.

The aim could not have been more accurate. The subsequent incidents of the Wyoming massacre were of no interest to that Seneca warrior, for the sharp crack of the little weapon was scarcely more sudden than was the ending of his career."""

# Adding more text blobs to collection
TEXT_COLLECTION = [TEXT1, TEXT2, TEXT3, TEXT4] * 3


class MServer(object):
    """ MulitProcessing Manager Server """
            
    def make_server(self):
        """ 
        Create a manager for the server, listening on the given port.
        """
        job_q = Queue.Queue()
        result_q = Queue.Queue()
        class QueueManager(SyncManager): pass
        QueueManager.register('get_job_q', callable=lambda:job_q)
        QueueManager.register('get_result_q', callable=lambda:result_q)
        m = QueueManager(address=(IP_ADDRESS, PORT_NUM), authkey='rackspace')
        m.start()
        return m
        
    def run_server(self):
        manager = self.make_server()
        input_q = manager.get_job_q()      
        output_q = manager.get_result_q()
        input_len = len(TEXT_COLLECTION)    
        
	# The Text collections are split into chunks. Each chunk is pushed into the job queue.
        chunk_size = int(math.ceil(input_len / float(WORKERS_COUNT)))
        
	# Chunk size is taken as process number for client
        #input_q.insert(chunk_size)
        for i in range(0, input_len, chunk_size):
            input_q.put(TEXT_COLLECTION[i:i+chunk_size])
        
	# Wait until all results are ready in output_q    
        output = []
        counter = 0         
        print "Waiting for responses from workers...\n"
        while counter < input_len:
            data = output_q.get()
            if data <> - 1:
                #print "Got response from worker %s.\n" % str(counter+1)
                output.extend(data)
                counter += 1
        
	# Print a master collection of top 10 words with count
        self.printWordsCount(output)  
        
        # Sleep a bit before shutting down the server - to give clients time to
        # realize the job queue is empty and exit in an orderly way.
        time.sleep(2)
        manager.shutdown()
        
    
    def printWordsCount(self, result):
        out_dict = collections.OrderedDict()
        for i in result:    
            if i in out_dict.keys():
                out_dict[i] = out_dict[i] + 1
            else:
                out_dict[i] = 1
        print "Word \t\t Count"
        print "*" * 60
        counter = 0
        for k, v in out_dict.iteritems():
            if counter < 10:
                print "%s \t\t %s" % (k, str(v))
                counter += 1

if __name__ == '__main__':
    m_obj = MServer()
    print "Starting Server at %d port number.....\n" % PORT_NUM
    m_obj.run_server()
