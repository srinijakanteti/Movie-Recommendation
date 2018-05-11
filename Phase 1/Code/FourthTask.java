import java.util.Scanner;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Connection;
import java.sql.*;

class FourthTask{
	public static void pDiff1(String g1,String g2) throws SQLException, ClassNotFoundException {
		Class.forName("com.jdbc.sql.Driver");
		Connection con=DriverManager.getConnection("jdbc:mysql://localhost:3306/MWDPhase1","srinija","ajinirs");
		int r1j[]=genreMovies1(g1);
		int m1j[]=genreMovies1(g2);
		int R=r1j[834];
		int M=r1j[834]+m1j[834];
		r1j[834]=0;
		m1j[834]=0;
		double[] w1j=new double[834];
		for(int i=0;i<834;i++){
			w1j[1]=(Math.log(((r1j[i]*(R-r1j[i]))/((m1j[i]-r1j[i])*(M-m1j[i]-R+r1j[i]))))*(Math.abs((r1j[i]/R)-((m1j[i]-r1j[i])/(M-R)))));
			System.out.println(w1j[i]+" ");
		}
	}
	public static void pDiff2(String g1,String g2) throws SQLException, ClassNotFoundException {
		Class.forName("com.jdbc.sql.Driver");
		Connection con=DriverManager.getConnection("jdbc:mysql://localhost:3306/MWDPhase1","srinija","ajinirs");
		int r1j[]=genreMovies2(g1);
		int m1j[]=genreMovies2(g2);
		int R=r1j[558];
		int M=r1j[558]+m1j[558];
		r1j[558]=0;
		m1j[558]=0;
		double[] w1j=new double[558];
		for(int i=0;i<558;i++){
			w1j[1]=(Math.log((r1j[i]/(R-r1j[i]))/((m1j[i]-r1j[i])*(M-m1j[i]-R+r1j[i])))*(Math.abs((r1j[i]/R)-((m1j[i]-r1j[i])/(M-R)))));
			System.out.println(w1j[i]+" ");
		}
	}
	public static int[] genreMovies1(String g) throws SQLException{
			
			int[] alltags=new int[560];
			String movies[];
			int[] movie_tag_count=new int[560];
			int i=0;
			Connection con=DriverManager.getConnection("jdbc:mysql://localhost:3306/MWDPhase1","srinija","ajinirs");
			Statement st1=con.createStatement();
			ResultSet rs1=st1.executeQuery("select 'tagid' from 'genometags' order by 'tagid'");
			while(rs1.next()){
				i=i+1;
				alltags[i]=rs1.getInt(1);
			}
			Statement st2=con.createStatement();
			ResultSet rs2=st2.executeQuery("select 'genre', GROUP_CONCAT('movieid') from mlmovies where 'genre'="+g+" group by 'genre'");
			while(rs2.next()){
				movies=rs2.getString(2).split(",");
				for(int c=0;c<movies.length;c++){
					for(int d=0;d<558;d++){
						Statement st3=con.createStatement();
						ResultSet rs3=st3.executeQuery("select count(*) from 'mltags' where 'tagid'="+alltags[d]+" and 'movieid'="+movies[c]);	
						if(rs3.next()) movie_tag_count[d]=rs3.getInt(1);
						st3.close();
					}
				}
				movie_tag_count[558]=movies.length;
			}st2.close();
			return movie_tag_count;
	}
	public static int[] genreMovies2(String g) throws SQLException{
		int alltags[]=new int[560];
		String movies[];
		int[] movie_tag_count=new int[560];
		int i=0;
		Connection con=DriverManager.getConnection("jdbc:mysql://localhost:3306/MWDPhase1","srinija","ajinirs");
		Statement st1=con.createStatement();
		ResultSet rs1=st1.executeQuery("select 'tagid' from 'mltags' order by 'tagid'");
		while(rs1.next()){
			i=i+1;
			alltags[i]=rs1.getInt(1);
		}
		Statement st2=con.createStatement();
		ResultSet rs2=st2.executeQuery("select 'genre', GROUP_CONCAT('movieid') from 'movies' where 'genre'="+g+" group by 'genre'"); 
		while(rs2.next()){
			movies=rs2.getString(2).split(",");
			for(int c=0;c<movies.length;c++){
				for(int d=0;d<558;d++){
					Statement st3=con.createStatement();
					ResultSet rs3=st3.executeQuery("select count(*) from 'mlmovies' where 'tagid'!="+alltags[d]+" and 'movieid'="+movies[c]);
					if(rs3.next()) movie_tag_count[d]=rs3.getInt(1);
					st3.close();
				}
			}
			movie_tag_count[558]=movies.length;
		}st2.close();
		return movie_tag_count;
	}
	public float[] A1=new float[2560];
	public float[] A2=new float[2560];
	public void tfIdfDiff(float idf){
		for(int i=0;i<A1.length;i++){
			if(A1[i]==-1) A1[i]=0;
			if(A2[i]==-1) A2[i]=0;
			A1[i]=idf*A1[i];
			A2[i]=idf*A1[i];
		}
		for(int i=0;i<A1.length-1;i++)
			System.out.print(A1[i]-A2[i]+",");
		System.out.println(A1[A1.length-1]-A2[A2.length-1]);
		
	}
	public float idf(String[] g1,String[] g2){
		int alltags1[]=new int[2558];
		for(int i=0;i<2558;i++)
			alltags1[i]=-1;
		int tagcount2=0;
		for(int j=0;j<g1.length;j++){
			String t[]= g1[j].split(",");
			alltags1[Integer.parseInt(t[0])]=0;
			tagcount2++;
			A1[Integer.parseInt(t[0])]+=Float.parseFloat(t[1]);
		}
		for(int j=0;j<g2.length;j++){
			String t[]= g2[j].split(",");
			if(alltags1[Integer.parseInt(t[0])]!=0) tagcount2++;
			
			A2[Integer.parseInt(t[0])]=Float.parseFloat(t[1]);
		}
		return (float)Math.log(2558.0/tagcount2);
	}
	
	public static void main(String args[]) throws Exception {
		/*System.out.println("Enter genre1:");
		Scanner sc1=new Scanner(System.in);
		String g1=sc1.nextLine();
		System.out.println("Enter genre2:");
		Scanner sc2=new Scanner(System.in);
		String g2=sc2.nextLine();
		System.out.println("Enter vector model:");
		Scanner sc3=new Scanner(System.in);
		String vectormodel=sc3.nextLine();*/
		SecondTask s1=new SecondTask();
		s1.main(args);
		SecondTask s2=new SecondTask();
		s2.main(args);
		/*if(vectormodel.equals("tfidfdiff")) tfIdfDiff();
		if(vectormodel.equals("pdiff1")) pDiff1(g1,g2);
		if(vectormodel.equals("pdiff2")) pDiff2(g1,g2);*/
	}
}


			
		