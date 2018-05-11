import java.sql.*; 
import java.sql.SQLException; 
import java.util.Scanner;
import java.text.SimpleDateFormat;
class FirstTask{  
	public static float[] weights;
	public static void main(String args[]) throws Exception{
		System.out.println("Enter the actorid:");
		Scanner sc=new Scanner(System.in);
		String actorid=sc.nextLine();
		System.out.println("Enter vector model:");
		Scanner sc2=new Scanner(System.in);
		String vectormodel=sc2.nextLine();
		Class.forName("com.mysql.jdbc.Driver");  
			Connection con=DriverManager.getConnection("jdbc:mysql://localhost:3306/MWDPhase1?useSSL=false","srinija","ajinirs"); //establishing connection with database
			Statement st=con.createStatement();  
			ResultSet rs1=st.executeQuery("select GROUP_CONCAT('movieid'), 'actorid', GROUP_CONCAT('actor_movie_rank') from movie_actor where actorid="+actorid+" group by actorid"); //to retrieve all the movies and ranks of a given actor
			while(rs1.next()){
				String[] actorranks=rs1.getString(3).split(","); //stores the actor ranks in a list
				String[] actormovies=rs1.getString(1).split(","); //stores the movies in a list
				for(int c=0;c<actormovies.length;c++){
					Statement st2=con.createStatement();
					ResultSet rs2=st2.executeQuery("select 'movieid', GROUP_CONCAT('tagid'), GROUP_CONCAT('timestamp') from mltags where movieid="+actormovies[c]+" group by movieid"); //for a given movie, retrieves the tags and timestamps
					while(rs2.next()){
						String[] movietags=rs2.getString(2).split(","); //stores the tags in a list
						String[] tagtimestamps=rs2.getString(3).split(","); //stores the timestamps in a list
						float[] tsweight=new float[tagtimestamps.length];
						for(int i=0;i<tagtimestamps.length;i++) tsweight[i]=i; //initialize the timestamp weights to some value
						SimpleDateFormat sdf=new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
						for(int i=tagtimestamps.length-1;i>=0;i--){
							for(int j=1;j<=i;j++){
								if(sdf.parse(tagtimestamps[j-1]).after(sdf.parse(tagtimestamps[j]))) //sorts the timestamps of tags 
								{ 
									String temp1="";
									temp1=tagtimestamps[j-1];
									tagtimestamps[j-1]=tagtimestamps[j];
									tagtimestamps[j]=temp1;
									float temp2;
									temp2=tsweight[j-1]; //sorts the weights/priorities of timestamps
									tsweight[j-1]=tsweight[j];
									tsweight[j]=temp2;
								}
							}
						}
						for(int i=0;i<tagtimestamps.length;i++) tsweight[i]=(tsweight[i]+1)/tagtimestamps.length; //to compute weighted timestamps for each tag
						Statement st3=con.createStatement();
						ResultSet rs3=st3.executeQuery("select COUNT('movieid'), 'movieid' from 'movie_actor' where 'movieid'="+actormovies[c]); //to get the count of all movies of an actor
						rs3.next();
						float actorrank=Float.parseFloat(actorranks[c])/Float.parseFloat(rs3.getString(1)); //actor rank = (rank of the actor in that movie)/(number of actors in that movie)
						st3.close();
						weights=new float[tagtimestamps.length]; //the final weighted tag vectors to be computed
						for(int i=0;i<movietags.length;i++) weights[i]=tsweight[i]*actorrank; //multiplication is used as the combination function
						weights=tf(movietags,weights); //calls the method to compute tf
						if(vectormodel.equals("tf-idf")) tfIdf(weights);
						System.out.println(actorid);
				    	for(int k=0;k<movietags.length;k++)
				    		System.out.println(movietags[k]+","+weights[k]);
				    	
				    		
				    	}
					}
				}
			}

	public static float[] tf(String[] movietags2, float[] weights) throws SQLException{
					for(int i=0;i<movietags2.length;i++){
						String t=movietags2[i];
						int tagcount=0;
						for(int j=0;j<movietags2.length;j++){
							if(t==movietags2[j]) tagcount++; //to count the number of times a tag occurs 
						}
					System.out.println(movietags2[i]+" "+tagcount);
					Connection con=DriverManager.getConnection("jdbc:mysql://localhost:3306/MWDPhase1","srinija","ajinirs");
					Statement st4=con.createStatement();
					ResultSet rs4=st4.executeQuery("select GROUP_CONCAT('movieid') from 'mltags' where 'tagid'="+movietags2[i]); //retrieves the number of movies under that particular tag
					String myquery="select COUNT(*) from movie_actor where ";
					if(rs4.next()){
						String moviesundertag[]=rs4.getString(1).split(",");
						int k;
						for(k=0;k<moviesundertag.length-1;k++){
							  myquery=myquery+"'movieid'="+moviesundertag[k]+" or "; //results in the total number of movies an actor acted in under that particular tag
							  }
							  myquery=myquery+"'movieid'="+moviesundertag[k]; 
						//myquery=myquery+"`movieid`="+moviesundertag[k];
						//System.out.println(myquery);
					}
					st4.close();
					Connection con1=DriverManager.getConnection("jdbc:mysql://localhost:3306/MWDPhase1","srinija","ajinirs");
					Statement st5=con1.createStatement();
					ResultSet rs5=st5.executeQuery(myquery);
					rs5.next();
					int moviecount=rs5.getInt(1);
					float tf=(float)(tagcount/(moviecount*1.0)); //TF=number of times the given actor has appeared for movies under the given tag
					weights[i]=weights[i]*tf;
					System.out.println(weights[i]);
					}
					return weights;
				}
				public static float[] tfIdf(float[] weights){
					float IDF=(float)(Math.log(557/weights.length)); //IDF=(total number of tags)/(number of tags the actor has acted in)
					for(int i=0;i<weights.length;i++) weights[i]=weights[i]*IDF;
					return weights;
				}
				public void print() //prints the tag vectors in descending order
				{
					for(int i=0;i<weights.length;i++){
						for(int j=0;j<i;j++){
							if(weights[i]<weights[j]){
								float temp=weights[i];
								weights[i]=weights[j];
								weights[j]=temp;
							}
						}
					}
					for(int i=0;i<weights.length;i++){
							System.out.println(weights[i]);
					}
				}
		//	catch(Exception e) 
			//	System.out.println(e);
	}
					
					
					
					
						
					
					
					
				
								
						
									


