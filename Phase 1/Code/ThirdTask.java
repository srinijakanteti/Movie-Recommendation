import java.text.SimpleDateFormat;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.*;
import java.util.Scanner;
import java.text.ParseException;
public class ThirdTask {
	public static float[] weights;
	public static void main(String args[]) throws SQLException, ClassNotFoundException, ParseException {
		System.out.println("Enter the userid:");
		Scanner sc1=new Scanner(System.in);
		int userid=sc1.nextInt();
		System.out.println("Enter the vector model:");
		Scanner sc2=new Scanner(System.in);
		String vectormodel=sc2.nextLine();
		Class.forName("com.mysql.jdbc.Driver");
		Connection con=DriverManager.getConnection("jdbc:mysql://localhost:3306/MWDPhase1","srinija","ajinirs");
		Statement st1=con.createStatement();
		ResultSet rs1=st1.executeQuery("select GROUP_CONCAT('movieid'), 'userid' from 'mltags' where 'userid'="+userid+" group by 'userid'");
		while(rs1.next()){
			String[] movies=rs1.getString(2).split(",");
			for(int c=0;c<movies.length;c++){
				Statement st2=con.createStatement();
				ResultSet rs2=st2.executeQuery("select 'movieid', GROUP_CONCAT('tagid'), GROUP_CONCAT('timestamp') from 'mltags' where 'movieid="+movies[c]+" group by 'movieid'");
				while(rs2.next()){
					String[] tags=rs2.getString(2).split(",");
					String[] timestamps=rs2.getString(3).split(",");
					float tsweight[]=new float[timestamps.length];
					for(int i=0;i<timestamps.length;i++) tsweight[i]=i;
					SimpleDateFormat sdf=new SimpleDateFormat("MM/dd/yyyy h:m");
					for(int i=timestamps.length-1;i>=0;i--){
						for(int j=1;j<=i;j++){
							if(sdf.parse(timestamps[j-1]).after(sdf.parse(timestamps[j]))){
								String temp1="";
								temp1=timestamps[j-1];
								timestamps[j-1]=timestamps[j];
								timestamps[j]=temp1;
								float temp2;
								temp2=tsweight[j-1];
								tsweight[j-1]=tsweight[j];
								tsweight[j]=temp2;
							}
						}
					}
					for(int i=0;i<timestamps.length;i++) 
						tsweight[i]=(tsweight[i]+1)/timestamps.length;
					tsweight=tf(tags,tsweight);
					if(vectormodel.equals("tf-idf")) tfIdf(tsweight);
					System.out.println(userid);
					if(tags[0]!=""){
						for(int k=0;k<tags.length;k++)
							System.out.println(tags[k]+","+tsweight[k]);
				}
			}
			}}
	}
	public static float[] tf(String[] tags2, float[] weights) throws SQLException{
		for(int i=0;i<tags2.length;i++){
			String t=tags2[i];
			int tagcount=0;
			for(int j=0;j<tags2.length;j++){
				if(t.equals(tags2[j])) tagcount++;
			}
			System.out.println(tags2[i]+" "+tagcount);
			Connection con1=DriverManager.getConnection("jdbc:mysql://localhost:3306/MWDPhase1","srinija","ajinirs");
			Statement st3=con1.createStatement();
			ResultSet rs3=st3.executeQuery("select GROUP_CONCAT('movieid') from 'mltags' where 'tagid'="+tags2[i]);
			String myquery="select count(*) from 'movie_actor' where ";
			if(rs3.next()){
				String[] moviesundertag=rs3.getString(1).split(",");
				int k;
				for(k=0;k<moviesundertag.length;k++){
					myquery=myquery+"'movieid'="+moviesundertag[k]+" or ";
				}
				myquery=myquery+"'movieid'="+moviesundertag[k];
			}
			Connection con2=DriverManager.getConnection("jdbc:mysql://localhost:3306/MWDPhase1","srinija","ajinirs");
			Statement st4=con2.createStatement();
			ResultSet rs4=st4.executeQuery(myquery);
			rs4.next();
			int moviecount=rs4.getInt(1);
			float tf=(float)(tagcount/(moviecount*1.0));
			weights[i]=weights[i]*tf;
			System.out.println(weights[i]);
		}
		return weights;
	}
	public static float[] tfIdf(float[] weights){
		float IDF=(float)(Math.log(557/weights.length));
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
}
	
				
			
			
			
					
			
			
			
			
			
					
			
								
				
